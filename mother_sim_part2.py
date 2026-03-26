import numpy as np

# --- PHYSICAL CONSTANTS ---
M_EFF = 0.5
R_C = 4.2
G_BASE = 0.45
G_LHY = 0.28
U0 = 4.2
G3 = 0.08
H_BAR = 0.658
K_B_T_300K = 25.85
CAVITY_LIFETIME_BASE = 50.0

K = np.linspace(0.5, 50.0, 600)

def get_gamma(rho):
    """Calculates realistic collisional broadening."""
    base_gamma = H_BAR / CAVITY_LIFETIME_BASE
    broadening = 0.01 * np.log(1 + rho)
    return base_gamma + broadening

def calculate_physics_metrics(rho):
    """Calculates Dispersion, Roton Gap, and State."""
    gamma = get_gamma(rho)
    e_k = (K**2) / (2 * M_EFF)
    # Energy landscape
    u_k = G_BASE + U0 * (np.sin(K * R_C) / (K * R_C))
    lhy = 2.5 * G_LHY * (rho**1.5)
    
    # Bogoliubov dispersion with dynamic gamma
    energy_sq = e_k * (e_k + 2*rho*u_k + 3*G3*rho**2 + lhy) - (0.5j * gamma)**2
    energy = np.real(np.sqrt(energy_sq + 0j))
    
    # Gap check
    window = energy[5:150]
    gap = np.min(window)
    
    # State validation
    state = "SUPERSOLID" if (gap / max(energy[-1], 1e-9) < 0.88) else "LIQUID"
    
    return state, gap, gamma

def run_integrated_sim():
    print("--- MOTHER_SIM_PART2: FINAL DESIGN ANALYSIS ---")
    print(f"{'Rho':<8} | {'State':<10} | {'Hold Ratio':<12} | {'Therm TR':<10} | {'Verdict'}")
    print("-" * 65)
    
    # Sweep from 1.2 to 2.0 to find the Design Window
    for rho in np.linspace(1.2, 2.0, 15):
        state, gap, gamma = calculate_physics_metrics(rho)
        
        if state == "SUPERSOLID":
            # Calculate temporal and thermal stability metrics
            t_form = H_BAR / gap
            lifetime = H_BAR / gamma
            hold_ratio = lifetime / t_form
            thermal_tr = gap / K_B_T_300K
            
            # FINAL DECISION: Is the design viable at room temp?
            # Hold Ratio > 40 ensures bit longevity
            # Thermal TR > 0.05 ensures thermal noise resistance
            if hold_ratio > 40 and thermal_tr > 0.05:
                verdict = "DESIGN-READY"
            else:
                verdict = "UNSTABLE"
                
            print(f"{rho:<8.3f} | {state:<10} | {hold_ratio:<12.2f} | {thermal_tr:<10.4f} | {verdict}")
        else:
            print(f"{rho:<8.3f} | {state:<10} | {'N/A':<12} | {'N/A':<10} | ---")

if __name__ == "__main__":
    run_integrated_sim()