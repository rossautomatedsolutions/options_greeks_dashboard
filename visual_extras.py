import numpy as np
import plotly.graph_objects as go
from greeks_calculator import black_scholes_price, vega, gamma, vomma

def plot_3d_option_price_surface(option_type, K, T, r,
                                  price_range=np.linspace(10, 100, 30),
                                  vol_range=np.linspace(0.1, 0.6, 30)):
    X, Y = np.meshgrid(price_range, vol_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            S = X[i][j]
            sigma = Y[i][j]
            Z[i][j] = black_scholes_price(option_type, S, K, T, r, sigma)

    return _build_surface(X, Y, Z, "Option Price", "Underlying Price", "Volatility", "Option Price")

def plot_3d_vega_surface(K, T, r,
                         price_range=np.linspace(10, 100, 30),
                         vol_range=np.linspace(0.1, 0.6, 30)):
    X, Y = np.meshgrid(price_range, vol_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i][j] = vega(X[i][j], K, T, r, Y[i][j])

    return _build_surface(X, Y, Z, "Vega", "Underlying Price", "Volatility", "Vega")

def plot_3d_gamma_surface(K, T, r, sigma,
                          price_range=np.linspace(10, 100, 30),
                          time_range=None):
    if time_range is None:
        time_range = np.linspace(0.01, T, 30)

    X, Y = np.meshgrid(price_range, time_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i][j] = gamma(X[i][j], K, Y[i][j], r, sigma)

    return _build_surface(X, Y, Z, "Gamma", "Underlying Price", "Time to Expiration", "Gamma")

def plot_3d_vomma_surface(K, T, r,
                          price_range=np.linspace(10, 100, 30),
                          vol_range=np.linspace(0.1, 0.6, 30)):
    X, Y = np.meshgrid(price_range, vol_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i][j] = vomma(X[i][j], K, T, r, Y[i][j])

    return _build_surface(X, Y, Z, "Vomma", "Underlying Price", "Volatility", "Vomma")

def _build_surface(X, Y, Z, title, x_label, y_label, z_label):
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label
        ),
        template="plotly_white"
    )
    return fig



# if __name__ == "__main__":
#     fig = plot_3d_option_price_surface("call", K=100, T=30/365, r=0.01)
#     fig.show()