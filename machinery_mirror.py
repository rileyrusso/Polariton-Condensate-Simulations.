import numpy as np
import matplotlib.pyplot as plt

# --- HARDWARE CONSTRAINTS (The "Mirror") ---
time_steps = np.linspace(0, 100, 200) # Time in picoseconds
leakage_rate = 0.02 # Density loss over time
thermal_rise = 0.005 # Heating per picosecond

# Initial Values
rho_t = 1.2
gamma_t = 0.05
U0 = 4.0

viability_range = []

print(f"Simulating Hardware Decay...")
for t in time_steps:
    # Mirror the reality: Density drops, Heat (gamma) rises
    current_rho = rho_t * np.exp(-leakage_rate * t)
    current_gamma = gamma_t + (thermal_rise * t)
    
    # Check physics at this micro-second
    E_k = (5.0**2) / 1.0 # Checking at a critical momentum k=5
    U_k = 0.4 + U0 * (np.sin(5.0 * 1.4) / (5.0 * 1.4))
    lhy = 2.5 * 0.25 * (current_rho**1.5)
    
    stability = E_k * (E_k + 2 * current_rho * U_k + 3 * 0.05 * current_rho**2 + lhy) - (0.5j * current_gamma)**2
    
    if np.imag(np.sqrt(stability + 0j)) < 1e-4:
        viability_range.append((t, current_rho, current_gamma))

if viability_range:
    t_start, t_end = viability_range[0][0], viability_range[-1][0]
    print(f"\n--- HARDWARE VIABILITY REPORT ---")
    print(f"Stable Window Duration: {t_end - t_start:.2f} ps")
    print(f"Safe Density Range: {viability_range[-1][1]:.3f} to {viability_range[0][1]:.3f}")
    print(f"Max Operating Temp (effective): {viability_range[-1][2]:.3f}")
else:
    print("CRITICAL FAILURE: System collapses immediately under hardware noise.")