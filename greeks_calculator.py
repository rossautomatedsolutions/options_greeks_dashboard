import numpy as np
from scipy.stats import norm

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def black_scholes_price(option_type, S, K, T, r, sigma):
    D1, D2 = d1(S, K, T, r, sigma), d2(S, K, T, r, sigma)
    if option_type.lower() == 'call':
        return S * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)

def delta(option_type, S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return norm.cdf(D1) if option_type.lower() == 'call' else -norm.cdf(-D1)

def gamma(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return norm.pdf(D1) / (S * sigma * np.sqrt(T))

def theta(option_type, S, K, T, r, sigma):
    D1, D2 = d1(S, K, T, r, sigma), d2(S, K, T, r, sigma)
    term1 = - (S * norm.pdf(D1) * sigma) / (2 * np.sqrt(T))
    if option_type.lower() == 'call':
        return term1 - r * K * np.exp(-r * T) * norm.cdf(D2)
    else:
        return term1 + r * K * np.exp(-r * T) * norm.cdf(-D2)

def vega(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(D1) * np.sqrt(T) / 100

def rho(option_type, S, K, T, r, sigma):
    D2 = d2(S, K, T, r, sigma)
    factor = K * T * np.exp(-r * T)
    return factor * norm.cdf(D2) / 100 if option_type.lower() == 'call' else -factor * norm.cdf(-D2) / 100

# --- Second Order Greeks ---

def vanna(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return (norm.pdf(D1) * np.sqrt(T) * (1 - D1 / (sigma * np.sqrt(T)))) / 100

def vomma(S, K, T, r, sigma):
    D1, D2 = d1(S, K, T, r, sigma), d2(S, K, T, r, sigma)
    return (vega(S, K, T, r, sigma) * 100) * D1 * D2 / sigma / 100

def charm(option_type, S, K, T, r, sigma):
    D1, D2 = d1(S, K, T, r, sigma), d2(S, K, T, r, sigma)
    part1 = norm.pdf(D1) * (2 * r * T - D2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T))
    return -part1 - r * norm.cdf(D1) if option_type.lower() == 'call' else -part1 + r * norm.cdf(-D1)

def speed(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    g = gamma(S, K, T, r, sigma)
    return -g / S * (D1 / (sigma * np.sqrt(T)) + 1)

def zomma(S, K, T, r, sigma):
    D1, D2 = d1(S, K, T, r, sigma), d2(S, K, T, r, sigma)
    return gamma(S, K, T, r, sigma) * ((D1 * D2 - 1) / sigma)
