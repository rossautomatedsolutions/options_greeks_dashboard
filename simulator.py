from greeks_calculator import *

def simulate_greek_vs_price(option_type, K, T, r, sigma, price_range):
    data = []
    for S in price_range:
        data.append({
            'S': S,
            'price': black_scholes_price(option_type, S, K, T, r, sigma),
            'delta': delta(option_type, S, K, T, r, sigma),
            'gamma': gamma(S, K, T, r, sigma),
            'theta': theta(option_type, S, K, T, r, sigma),
            'vega': vega(S, K, T, r, sigma),
            'rho': rho(option_type, S, K, T, r, sigma),
            'vanna': vanna(S, K, T, r, sigma),
            'vomma': vomma(S, K, T, r, sigma),
            'charm': charm(option_type, S, K, T, r, sigma),
            'speed': speed(S, K, T, r, sigma),
            'zomma': zomma(S, K, T, r, sigma),
        })
    return data
