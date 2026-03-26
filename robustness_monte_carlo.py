import numpy as np

# --- SETTINGS ---
ITERATIONS = 1000
STABILITY_THRESHOLD = 1e-4

# Base Physics Values
m_eff, g, rho0_base, U0_base, Rc, gamma_base = 0.5, 0.4, 1.2, 4.0, 1.4, 0.05
g_lhy, g3 = 0.25, 0.05
k = np.linspace(1.0, 50.0, 500)

# Noise Levels (Standard Deviation)
laser_jitter = 0.05  # 5% fluctuation in density
power_drift = 0.1    # 10% fluctuation in interaction strength

def check_shot(rho, U0_val, gamma_val):
    E_k = (k**2) / (2 * m_eff)
    lhy_p = 2.5 * g_lhy * (rho**1.5)
    U_k = g + U0_val * (np.sin(k * Rc) / (k * Rc))
    # Bogoliubov Energy
    energy_sq = E_k * (E_k + 2 * rho * U_k + 3 * g3 * rho**2 + lhy_p) - (0.5j * gamma_val)**2
    # Return max instability
    return np.max(np.imag(np.sqrt(energy_sq + 0j)))

# --- RUN MONTE CARLO ---
success_count = 0
for _ in range(ITERATIONS):
    # Apply random noise to each parameter
    rho_noisy = np.random.normal(rho0_base, laser_jitter)
    u0_noisy = np.random.normal(U0_base, power_drift)
    gamma_noisy = np.random.normal(gamma_base, 0.01)
    
    if check_shot(rho_noisy, u0_noisy, gamma_noisy) < STABILITY_THRESHOLD:
        success_count += 1

survival_rate = (success_count / ITERATIONS) * 100
print(f"--- MONTE CARLO RESULTS ---")
print(f"Survival Probability: {survival_rate:.2f}%")
print(f"Status: {'EXPERIMENTAL GRADE' if survival_rate > 95 else 'TOO VOLATILE'}")