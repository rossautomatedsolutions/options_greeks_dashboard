from greeks_calculator import *
from simulator import simulate_greek_vs_price
import pprint

option_type = "call"
S = 100
K = 100
T = 30 / 365
r = 0.01
sigma = 0.25

print("--- Single Greek Outputs ---")
print(f"Price: {black_scholes_price(option_type, S, K, T, r, sigma):.4f}")
print(f"Delta: {delta(option_type, S, K, T, r, sigma):.4f}")
print(f"Gamma: {gamma(S, K, T, r, sigma):.4f}")
print(f"Theta: {theta(option_type, S, K, T, r, sigma):.4f}")
print(f"Vega : {vega(S, K, T, r, sigma):.4f}")
print(f"Rho  : {rho(option_type, S, K, T, r, sigma):.4f}")
print(f"Vanna: {vanna(S, K, T, r, sigma):.4f}")
print(f"Vomma: {vomma(S, K, T, r, sigma):.4f}")
print(f"Charm: {charm(option_type, S, K, T, r, sigma):.4f}")
print(f"Speed: {speed(S, K, T, r, sigma):.4f}")
print(f"Zomma: {zomma(S, K, T, r, sigma):.4f}")

print("\n--- Simulation Test (Price Range) ---")
price_range = range(80, 121, 5)
sim_data = simulate_greek_vs_price(option_type, K, T, r, sigma, price_range)
pprint.pprint(sim_data[:3])  # Preview first few
