import numpy as np

# --- PHYSICAL CONSTANTS & LHY PARAMETERS ---
m_eff, g, rho0, U0, Rc, gamma = 0.5, 0.4, 1.2, 4.0, 1.4, 0.05
g_lhy = 0.25 # Quantum fluctuation strength (The "Noise" stabilizer)
k = np.linspace(1.0, 50.0, 500)

def check_stability(g3):
    E_k = (k**2) / (2 * m_eff)
    # The interaction potential including LHY quantum pressure
    # We add 2.5 * g_lhy * rho0^1.5 to the effective repulsion
    lhy_pressure = 2.5 * g_lhy * (rho0**1.5)
    
    U_k = g + U0 * (np.sin(k * Rc) / (k * Rc))
    
    # Bogoliubov Energy with LHY correction
    # The term 3*g3*rho0^2 + lhy_pressure ensures stability against collapse
    energy_sq = E_k * (E_k + 2 * rho0 * U_k + 3 * g3 * rho0**2 + lhy_pressure) - (0.5j * gamma)**2
    
    # Use np.sqrt on complex energy_sq. Real part = excitation, Imaginary = decay/instability
    energy = np.sqrt(energy_sq)
    
    # Return the maximum growth rate (Imaginary part). 
    # If this is positive, the system is unstable (noise is growing).
    return np.max(np.imag(energy))

# --- RUN SEARCH ---
g3_range = np.linspace(0, 0.5, 100)
for val in g3_range:
    instability = check_stability(val)
    # Stability criterion: Instability (growth rate) must be near zero
    if instability < 1e-4:
        print(f"-------------------------------------")
        print(f"STABILIZED BY LHY: g3 = {val:.4f}")
        print(f"-------------------------------------")
        break