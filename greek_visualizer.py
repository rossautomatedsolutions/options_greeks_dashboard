import plotly.graph_objects as go
import numpy as np

def plot_greek(data, greek_name):
    x = [d['S'] for d in data]
    y = [d[greek_name] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=greek_name))
    fig.update_layout(title=f"{greek_name.capitalize()} vs Underlying Price",
                      xaxis_title="Underlying Price",
                      yaxis_title=greek_name.capitalize(),
                      template="plotly_white")
    return fig

def plot_all_greeks(data, greek_list):
    fig = go.Figure()
    x = [d['S'] for d in data]
    for greek in greek_list:
        y = [d[greek] for d in data]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=greek.capitalize()))
    fig.update_layout(title="Greeks vs Underlying Price",
                      xaxis_title="Underlying Price",
                      yaxis_title="Value",
                      template="plotly_white")
    return fig

def plot_payoff(option_type, K, price_range, premium):
    """
    Plots the profit/loss at expiration for a single long call or put.
    """
    x = np.array(price_range)

    if option_type.lower() == "call":
        y = np.maximum(x - K, 0) - premium
    else:
        y = np.maximum(K - x, 0) - premium

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='P&L'))

    fig.update_layout(
        title="P&L Payoff at Expiration",
        xaxis_title="Underlying Price at Expiration",
        yaxis_title="Profit / Loss",
        template="plotly_white"
    )
    return fig