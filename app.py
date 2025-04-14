import streamlit as st
import numpy as np
import plotly.graph_objects as go

from simulator import simulate_greek_vs_price
from greek_visualizer import plot_greek, plot_all_greeks, plot_payoff
from visual_extras import (
    plot_3d_option_price_surface,
    plot_3d_vega_surface,
    plot_3d_gamma_surface,
    plot_3d_vomma_surface
)
from greeks_calculator import black_scholes_price
from option_utils import convert_days_to_years, convert_percent_to_decimal

# --- Layout config ---
st.set_page_config(page_title="Options Greeks Visualizer", layout="wide")
st.title("📈 Options Greeks Educational Dashboard")

# --- Sidebar Inputs ---
st.sidebar.header("Option Inputs")
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
underlying_price = st.sidebar.slider("Underlying Price (S)", 10, 100, 50)
strike_price = st.sidebar.slider("Strike Price (K)", 10, 100, 50)
days = st.sidebar.slider("Days to Expiration", 1, 90, 30)
iv = st.sidebar.slider("Implied Volatility (%)", 1.0, 100.0, 25.0)
rfr = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 10.0, 1.0)

# --- Conversions ---
T = convert_days_to_years(days)
sigma = convert_percent_to_decimal(iv)
r = convert_percent_to_decimal(rfr)
price_range = np.linspace(underlying_price * 0.8, underlying_price * 1.2, 50)

# --- Dropdown for Greek Display ---
greek_view = st.selectbox("Greeks to Display", [
    "All Greeks", "First-Order Greeks", "Second-Order Greeks",
    "Delta", "Gamma", "Theta", "Vega", "Rho",
    "Vanna", "Vomma", "Charm", "Speed", "Zomma",
    "Price Only"
])

# --- Toggle for 3D Plots ---
show_surface = st.checkbox("✅ Show 3D Surface Plots")

# --- Simulate data ---
data = simulate_greek_vs_price(option_type, strike_price, T, r, sigma, price_range)

# --- Determine Greeks to Plot ---
if greek_view == "All Greeks":
    selected = ['delta', 'gamma', 'theta', 'vega', 'rho',
                'vanna', 'vomma', 'charm', 'speed', 'zomma']
elif greek_view == "First-Order Greeks":
    selected = ['delta', 'gamma', 'theta', 'vega', 'rho']
elif greek_view == "Second-Order Greeks":
    selected = ['vanna', 'vomma', 'charm', 'speed', 'zomma']
elif greek_view != "Price Only":
    selected = [greek_view.lower()]
else:
    selected = []

# --- Combined Greek Chart ---
if selected:
    st.subheader("📊 Combined Greek Chart")
    fig = plot_all_greeks(data, selected)
    st.plotly_chart(fig, use_container_width=True)

# --- Dashboard: Individual Greek Charts ---
if selected:
    st.subheader("📉 Individual Greek Charts")
    cols = st.columns(3)  # 3 charts per row
    for idx, g in enumerate(selected):
        with cols[idx % 3]:
            st.markdown(f"**{g.capitalize()}**")
            fig = plot_greek(data, g)
            st.plotly_chart(fig, use_container_width=True, height=250)

# --- Payoff Diagram ---
st.subheader("💵 Payoff at Expiration")
premium = black_scholes_price(option_type, underlying_price, strike_price, T, r, sigma)
fig = plot_payoff(option_type, strike_price, price_range, premium)
st.plotly_chart(fig, use_container_width=True)

# --- Dashboard: 3D Surface Plots ---
if show_surface:
    st.subheader("🧊 3D Surface Charts")

    surface_funcs = [
        ("Option Price", lambda: plot_3d_option_price_surface(option_type, strike_price, T, r)),
        ("Vega", lambda: plot_3d_vega_surface(strike_price, T, r)),
        ("Gamma", lambda: plot_3d_gamma_surface(strike_price, T, r, sigma)),
        ("Vomma", lambda: plot_3d_vomma_surface(strike_price, T, r)),
    ]

    cols = st.columns(2)  # 2 plots per row
    for idx, (name, func) in enumerate(surface_funcs):
        with cols[idx % 2]:
            st.markdown(f"**{name} Surface**")
            try:
                fig = func()
                st.plotly_chart(fig, use_container_width=True, height=300)
            except Exception as e:
                st.error(f"{name} surface error: {e}")
