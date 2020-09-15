"""
This script contains useful function to evaluate predictions
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Metrics:
    """
    Class to handle metrics computation for the backtesting
    """

    def __init__(self, eval_demand: pd.DataFrame) -> None:

        self.df = eval_demand

        # Metrics
        self.bias = 100 * calculate_bias(
            eval_demand.demand, eval_demand.demand_act
        )
        self.smape = 100 * calculate_smape(
            eval_demand.demand, eval_demand.demand_act
        )


def calculate_bias(x, y) -> float:
    """Compute bias between prediction and actual"""
    if np.sum(x) == 0 and np.sum(y) == 0:
        return 0
    elif np.sum(x) == 0:
        return -np.inf
    elif np.sum(y) == 0:
        return np.inf
    return float(np.log(np.sum(x) / np.sum(y)))


def calculate_smape(x, y):
    """Copute smape between predictino and actual"""
    if np.sum(x) == 0 and np.sum(y) == 0:
        return 0
    elif np.sum(x + y) == 0:
        return np.inf
    return np.sum(np.abs(x - y) / np.sum((x + y) / 2))


def plot_metrics(metrics: Metrics) -> plt.Figure:
    """
    Plot global metrics
    """
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(
        0.1, 0.4, f"Smape: {round(metrics.smape, 2)}%", ha='left'
    )
    ax.text(
        0.1, 0.6, f"Bias: {round(metrics.bias, 2)}%", ha='left'
    )
    ax.axis('off')
    plt.tight_layout()
    return fig


def plot_sales_evol(df: pd.DataFrame) -> plt.Figure:
    """
    Plot prediction and actual evolution
    """
    # Aggregate prediction and actual
    df_agg = (
        df
        .groupby(["week_id"], as_index=False)
        [["demand", "demand_act"]]
        .agg("sum")
        .sort_values(by=["week_id"])
    )

    # Plot prediction and actual
    fig = plt.figure(figsize=(15, 10))
    plt.plot(
        df_agg.week_id, df_agg.demand,
        color="green", label="prediction", linewidth=5
    )
    plt.plot(
        df_agg.week_id, df_agg.demand_act
        , color="gray", label="actual", linewidth=5
    )
    plt.xlabel("Week id")
    plt.ylabel("Pieces")
    plt.legend()
    return fig
