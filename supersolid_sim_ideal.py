import numpy as np
import matplotlib.pyplot as plt

# --- PHYSICS PARAMETERS (Your Research Setup) ---
m_eff = 0.5    # Effective mass (Polariton)
g = 0.4        # Local repulsion (2-body)
rho0 = 1.2     # Density
U0 = 4.0       # Solid-forming force (Lattice strength)
Rc = 1.4       # Interaction range
g3 = 0.1       # 3-body Stabilizer (The "Dirac Fix")

# --- DATA GENERATION FUNCTIONS ---
def get_energy(k_vals, temp_gamma):
    E_k = (k_vals**2) / (2 * m_eff)
    U_k = g + U0 * (np.sin(k_vals * Rc) / (k_vals * Rc))
    # Bogoliubov Equation with 3-body term and decay
    energy_sq = E_k * (E_k + 2 * rho0 * U_k + 3 * g3 * rho0**2) - (0.5j * temp_gamma)**2
    return np.sqrt(energy_sq)

k = np.linspace(1.0, 50.0, 500)

# --- CREATE MULTI-GRAPH DASHBOARD ---
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle(f"Photonic Supersolid Simulation (U0={U0}, g3={g3})", fontsize=16)

# GRAPH 1: THE DISPERSION (Momentum Graph)
# This shows the "Roton" dip - the fingerprint of the solid.
base_energy = get_energy(k, 0.05)
axs[0].plot(k, np.real(base_energy), color='blue', lw=2, label="Real Energy")
axs[0].plot(k, np.imag(base_energy), color='red', ls='--', alpha=0.6, label="Instability")
axs[0].set_title("1. Momentum Dispersion (4K)")
axs[0].set_xlabel("Momentum (k)")
axs[0].set_ylabel("Energy (ω)")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

# GRAPH 2: THERMAL MELTING (Temperature Sweep)
# Watch the 'dip' fill in as the system loses its crystal structure.
temps = [4, 77, 150, 300]
for T in temps:
    # Aggressive decay scale to see the change
    gamma_T = 0.05 + (T / 20) 
    e_T = get_energy(k, gamma_T)
    axs[1].plot(k, np.real(e_T), label=f"{T} K")
axs[1].set_title("2. Thermal Melting Phase")
axs[1].set_xlabel("Momentum (k)")
axs[1].set_ylabel("Energy (ω)")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

# GRAPH 3: LATTICE STABILITY HEATMAP
# This shows how "stiff" the crystal is at different densities.
rhos = np.linspace(0.5, 2.5, 100)
stability_matrix = []
for r in rhos:
    # Check the depth of the roton at different densities
    e_rho = (k**2)/(2*m_eff) * ((k**2)/(2*m_eff) + 2*r*(g + U0*(np.sin(k*Rc)/(k*Rc))) + 3*g3*r**2)
    stability_matrix.append(np.min(e_rho))

axs[2].fill_between(rhos, stability_matrix, color='green', alpha=0.3)
axs[2].plot(rhos, stability_matrix, color='darkgreen')
axs[2].axhline(0, color='black', lw=1)
axs[2].set_title("3. Global Stability vs Density")
axs[2].set_xlabel("Fluid Density (ρ)")
axs[2].set_ylabel("Min Energy^2 (Stability)")
axs[2].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# --- FINAL ANALYSIS OUTPUT ---
k_roton = k[np.argmin(np.real(base_energy))]
d = (2 * np.pi) / k_roton
print(f"\n--- RESEARCH SUMMARY ---")
print(f"Lattice Spacing: {d:.4f} micrometers")
print(f"Predicted State: {'Stable Supersolid' if np.min(stability_matrix) > 0 else 'Unstable/Collapsed'}")
print(f"Critical Momentum (k): {k_roton:.2f}")