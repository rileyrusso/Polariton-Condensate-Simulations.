import numpy as np
import matplotlib.pyplot as plt

# --- PHYSICS PARAMETERS ---
m_eff = 0.5    
g = 0.4        # 2-body repulsion
rho0 = 1.2     # Density
U0 = 4.0      # Lattice strength
Rc = 1.4        # Interaction range
g3 = 0.00      # 3-body term (reduced to see LHY effect)

# --- NEW: LHY PARAMETERS ---
# This is the "Quantum Noise" stabilizer strength
g_lhy = 0.25   

def get_energy(k_vals, temp_gamma, rho):
    E_k = (k_vals**2) / (2 * m_eff)
    U_k = g + U0 * (np.sin(k_vals * Rc) / (k_vals * Rc))
    
    # LHY Correction: Represents the sum of zero-point fluctuations
    # It scales non-linearly with density, acting as a "quantum pressure"
    lhy_term = g_lhy * (rho**1.5)
    
    # Updated Bogoliubov Equation:
    # We include the LHY term to combat the 'collapse' at high densities
    energy_sq = E_k * (E_k + 2 * rho * U_k + 3 * g3 * rho**2 + 2.5 * lhy_term) - (0.5j * temp_gamma)**2
    return np.sqrt(energy_sq)

k = np.linspace(1.0, 50.0, 500)

# --- DASHBOARD GENERATION ---
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle(f"Quantum Droplet Simulation (LHY Optimized, g_lhy={g_lhy})", fontsize=16)

# 1. MOMENTUM DISPERSION
base_energy = get_energy(k, 0.05, rho0)
axs[0].plot(k, np.real(base_energy), color='blue', lw=2, label="Real Energy")
axs[0].plot(k, np.imag(base_energy), color='red', ls='--', alpha=0.6, label="Instability")
axs[0].set_title("1. LHY-Stabilized Dispersion")
axs[0].set_xlabel("Momentum (k)")
axs[0].set_ylabel("Energy (ω)")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

# 2. THERMAL MELTING
temps = [4, 77, 150, 300]
for T in temps:
    gamma_T = 0.05 + (T / 15) # More realistic thermal decay for room-temp testing
    e_T = get_energy(k, gamma_T, rho0)
    axs[1].plot(k, np.real(e_T), label=f"{T} K")
axs[1].set_title("2. Thermal Stability (LHY vs Heat)")
axs[1].set_xlabel("Momentum (k)")
axs[1].set_ylabel("Energy (ω)")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

# 3. STABILITY VS DENSITY (The "Phase Diagram")
rhos = np.linspace(0.1, 3.0, 100)
min_energy_sq = []
for r in rhos:
    # Recalculate minimum stability for each density
    energy_test = get_energy(k, 0.05, r)
    min_energy_sq.append(np.min(np.real(energy_test)**2))

axs[2].fill_between(rhos, min_energy_sq, color='purple', alpha=0.2)
axs[2].plot(rhos, min_energy_sq, color='purple', lw=2)
axs[2].axhline(0, color='black', lw=1)
axs[2].set_title("3. Global Stability Window")
axs[2].set_xlabel("Fluid Density (ρ)")
axs[2].set_ylabel("Min Stability")
axs[2].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()