import numpy as np

# Physical constants
H_BAR = 0.658 # meV * ps
CAVITY_LIFETIME_BASE = 50.0  # ps (Standard high-Q perovskite microcavity)

def get_gamma(rho):
    """
    Realistic decay function: 
    Leakage increases as density increases due to collisional broadening.
    """
    base_gamma = H_BAR / CAVITY_LIFETIME_BASE
    # Collision-induced broadening (logarithmic increase with density)
    broadening = 0.01 * np.log(1 + rho) 
    return base_gamma + broadening

def check_leakage_dynamics(rho):
    gamma = get_gamma(rho)
    lifetime = H_BAR / gamma
    
    # We'll re-calculate the Roton Gap here to see if the solid forms 
    # faster than the "realistic" lifetime
    # (Assuming we have calculated gap from previous steps)
    # Using a representative gap based on our previous runs (~1.2 meV)
    gap = 1.2 
    t_form = H_BAR / gap
    
    hold_ratio = lifetime / t_form
    return lifetime, hold_ratio

def run_step4():
    print("--- STEP 4: REALISTIC LEAKAGE ANALYSIS ---")
    print(f"{'Rho':<8} | {'Gamma_0':<10} | {'Lifetime':<10} | {'Hold Ratio'}")
    print("-" * 55)
    
    for rho in np.linspace(1.0, 2.0, 10):
        gamma = get_gamma(rho)
        lifetime = H_BAR / gamma
        t_form = 0.55 # Average from previous steps
        hold_ratio = lifetime / t_form
        
        print(f"{rho:<8.3f} | {gamma:<10.4f} | {lifetime:<10.2f} | {hold_ratio:.2f}")

if __name__ == "__main__":
    run_step4()