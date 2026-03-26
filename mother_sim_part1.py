import numpy as np
from dataclasses import dataclass, asdict

# ============================================================
# MOTHER SIM FOR "SOLID LIGHT" / PHOTONIC SUPERSOLID RESEARCH
# ============================================================
# Honest design:
# 1) A toy stability model explores parameter space.
# 2) A milestone engine maps simulated behavior onto the
# experimental pipeline researchers actually follow.
# 3) A literature clamp prevents the simulation from claiming
# achievements beyond what has actually been demonstrated.
# ============================================================

# -----------------------
# HARDWARE / MODEL CONSTS
# -----------------------
M_EFF = 0.5
R_C = 3.5
GAMMA = 0.05
G_LHY = 0.28
K_GRID = np.linspace(1.0, 50.0, 600)

# -----------------------
# RESEARCH STATUS CLAMP
# -----------------------
# Highest experimentally supported stage to date.
# 0: no platform
# 1: strong coupling achieved
# 2: polariton condensation achieved
# 3: supersolid signatures achieved
# 4: room-temperature supersolid achieved
# 5: self-bound photonic droplet achieved
# 6: robust device-grade stable solid light achieved
CURRENT_RESEARCH_STAGE = 4

RESEARCH_STAGE_LABELS = {
    0: "No validated platform",
    1: "Strong light-matter coupling demonstrated",
    2: "Polariton condensation demonstrated",
    3: "Photonic supersolid signatures demonstrated",
    4: "Room-temperature photonic supersolidity demonstrated",
    5: "Self-bound photonic droplet demonstrated",
    6: "Device-grade stable solid light achieved",
}

@dataclass
class SimResult:
    u0: float
    g_base: float
    g3: float
    survival_pct: float
    viability_window_ps: float
    spacing_um: float | None
    raw_stage: int
    clamped_stage: int
    raw_stage_label: str
    clamped_stage_label: str
    notes: list[str]

# -----------------------
# CORE TOY PHYSICS MODEL
# -----------------------
def calculate_stability(rho: float, g3_val: float, g_base: float, u0_val: float, gamma_val: float) -> int:
    """
    Returns:
      0 = unstable
      1 = metastable / no useful roton minimum
      2 = roton-softened stable window
      3 = strongly self-bound-like heuristic regime (toy only)
    """
    e_k = (K_GRID**2) / (2 * M_EFF)
    lhy_pressure = 2.5 * G_LHY * (rho**1.5)

    # IMPORTANT FIX: g_base now actually enters the interaction kernel
    u_k = g_base + u0_val * (np.sin(K_GRID * R_C) / (K_GRID * R_C))

    energy_sq = e_k * (
        e_k + 2 * rho * u_k + 3 * g3_val * rho**2 + lhy_pressure
    ) - (0.5j * gamma_val)**2

    energy = np.sqrt(energy_sq + 0j)

    # hard instability check
    if np.max(np.imag(energy)) > 0.032:
        return 0

    real_energy = np.real(energy)
    window = real_energy[30:250]
    min_idx = np.argmin(window)

    if min_idx == 0 or min_idx == len(window) - 1:
        return 1

    depth_ratio = window[min_idx] / max(real_energy[-1], 1e-9)

    # roton-like dip
    if depth_ratio < 0.88:
        # very deep dip heuristic -> "droplet-like" toy flag
        if depth_ratio < 0.55 and gamma_val < 0.03 and rho > 1.0:
            return 3
        return 2

    return 1

def run_diagnostics(u0: float, g_base: float, g3_target: float) -> tuple[float, float, int]:
    """
    Returns:
      survival_pct, viability_window_ps, strongest_regime
    """
    successes = 0
    strongest_regime = 0

    for _ in range(300):
        n_rho = np.random.normal(1.1, 0.1)
        regime = calculate_stability(n_rho, g3_target, g_base, u0, GAMMA)
        strongest_regime = max(strongest_regime, regime)
        if regime >= 2:
            successes += 1

    survival = (successes / 300.0) * 100.0

    time_ps = np.linspace(0, 150, 75)
    window = 0.0

    for t in time_ps:
        rho_t = 1.1 * np.exp(-0.020 * t)
        gamma_t = GAMMA + (0.003 * t)
        regime = calculate_stability(rho_t, g3_target, g_base, u0, gamma_t)
        strongest_regime = max(strongest_regime, regime)

        if regime >= 2:
            window = float(t)
        else:
            break

    return survival, window, strongest_regime

def estimate_spacing(g_base: float, u0: float, g3_val: float, rho: float = 1.1) -> float | None:
    """
    Estimates lattice spacing from roton minimum in the toy dispersion.
    """
    e_k = (K_GRID**2) / (2 * M_EFF)
    u_k = g_base + u0 * (np.sin(K_GRID * R_C) / (K_GRID * R_C))
    lhy_pressure = 2.5 * G_LHY * (rho**1.5)

    e_final = np.real(np.sqrt(
        e_k * (e_k + 2*rho*u_k + 3*g3_val*rho**2 + lhy_pressure) + 0j
    ))

    region = e_final[30:250]
    idx_local = np.argmin(region)
    idx = 30 + idx_local

    if idx <= 0 or idx >= len(K_GRID):
        return None

    k_star = K_GRID[idx]
    return float((2 * np.pi) / k_star)

# -----------------------
# RESEARCH PIPELINE LOGIC
# -----------------------
def infer_research_stage(
    survival_pct: float,
    viability_window_ps: float,
    strongest_regime: int,
    room_temp: bool = False
) -> tuple[int, list[str]]:
    """
    Maps toy outputs to a research milestone sequence.
    """
    notes = []

    # Baseline assumption: we are working in a polaritonic platform
    stage = 2
    notes.append("Assumed polaritonic platform with condensation-stage capability.")

    # Supersolid-like signatures
    if survival_pct > 40 and viability_window_ps > 10 and strongest_regime >= 2:
        stage = 3
        notes.append("Toy model reached roton-softened stable window consistent with supersolid-like signatures.")

    # Room-temp marker is an experimental flag, not something the toy model proves
    if room_temp and stage >= 3:
        stage = 4
        notes.append("Room-temperature supersolid flag enabled.")

    # Self-bound droplet-like regime in toy model
    if survival_pct > 85 and viability_window_ps > 80 and strongest_regime >= 3:
        stage = 5
        notes.append("Toy model entered a self-bound-like regime, but this exceeds settled experimental status unless externally validated.")

    # Device-grade stable solid light would require much stricter criteria
    if survival_pct > 95 and viability_window_ps > 120 and strongest_regime >= 3:
        stage = 6
        notes.append("Toy model suggests device-grade regime, but this is purely hypothetical here.")

    return stage, notes

# -----------------------
# AUTO-TUNER
# -----------------------
def find_golden_profile(max_tests: int = 100):
    print("STARTING HEURISTIC SWEEP...")
    print(f"{'Test':<5} | {'U0':<6} | {'G_BASE':<8} | {'Survive':<10} | {'Window':<10} | {'Regime':<6}")
    print("-" * 72)

    test_count = 0
    u0_space = np.linspace(2.5, 4.5, 10)
    gbase_space = np.linspace(0.45, 0.65, 10)
    g3_fixed = 0.08

    best = None
    best_score = -np.inf

    for u0 in u0_space:
        for gb in gbase_space:
            test_count += 1
            surv, win, regime = run_diagnostics(u0, gb, g3_fixed)

            print(f"{test_count:<5} | {u0:.2f} | {gb:.2f} | {surv:>6.1f}% | {win:>6.1f} ps | {regime:<6}")

            score = surv + 0.5 * win + 10 * regime
            if score > best_score:
                best_score = score
                best = (u0, gb, g3_fixed, surv, win, regime)

            if test_count >= max_tests:
                return best

    return best

# -----------------------
# MASTER EXECUTION
# -----------------------
def run_mother_sim(room_temp_flag: bool = True) -> SimResult:
    best = find_golden_profile()

    if best is None:
        return SimResult(
            u0=np.nan,
            g_base=np.nan,
            g3=np.nan,
            survival_pct=0.0,
            viability_window_ps=0.0,
            spacing_um=None,
            raw_stage=0,
            clamped_stage=0,
            raw_stage_label=RESEARCH_STAGE_LABELS[0],
            clamped_stage_label=RESEARCH_STAGE_LABELS[0],
            notes=["No viable heuristic profile found in sweep."]
        )

    u0_f, gb_f, g3_f, surv_f, win_f, regime_f = best
    spacing = estimate_spacing(gb_f, u0_f, g3_f)

    raw_stage, notes = infer_research_stage(
        survival_pct=surv_f,
        viability_window_ps=win_f,
        strongest_regime=regime_f,
        room_temp=room_temp_flag
    )

    clamped_stage = min(raw_stage, CURRENT_RESEARCH_STAGE)

    if raw_stage > clamped_stage:
        notes.append(
            "Simulation entered a regime beyond current experimentally established research status; result clamped."
        )

    notes.append(
        f"Current literature clamp: {RESEARCH_STAGE_LABELS[CURRENT_RESEARCH_STAGE]}"
    )

    return SimResult(
        u0=u0_f,
        g_base=gb_f,
        g3=g3_f,
        survival_pct=surv_f,
        viability_window_ps=win_f,
        spacing_um=spacing,
        raw_stage=raw_stage,
        clamped_stage=clamped_stage,
        raw_stage_label=RESEARCH_STAGE_LABELS[raw_stage],
        clamped_stage_label=RESEARCH_STAGE_LABELS[clamped_stage],
        notes=notes
    )

# -----------------------
# DISPLAY
# -----------------------
if __name__ == "__main__":
    result = run_mother_sim(room_temp_flag=True)

    print("\nFINAL MOTHER-SIM RESULT")
    print("-" * 40)
    for k, v in asdict(result).items():
        print(f"{k}: {v}")