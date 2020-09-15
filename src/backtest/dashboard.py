"""
This script generates an HTML report with metrics (in backtest)
"""

import os
import pathlib as pl

import matplotlib.pyplot as plt
import pandas as pd

from src.services.service_provider import ServiceProviderHandler
from .utils import Metrics, plot_metrics, plot_sales_evol

SERVICE = ServiceProviderHandler()


class Dashboard():
    """
    Class enabling to generate a HTML dashboard
    """
    APP = pl.Path("app")
    PATH_TEMPLATE = os.path.join(os.path.dirname(__file__), "templates")
    PATH_STATIC = "static"
    PATH_TEMPLATES = "templates"
    CSS_TEMPLATE = "dashboard_style.css"
    HTML_TEMPLATE = "dashboard.html"

    def __init__(self, eval_demand: pd.DataFrame, metrics: Metrics):
        super().__init__()

        # DataFrame with predictions and actuals
        self.eval_demand = eval_demand

        # Metrics
        self.metrics = metrics

    def create_dashboard(self):
        """
        Generate the dashboard with the visualisations and the metrics
        """
        SERVICE.log.info(f"Creating dashboard")

        # Plot figures
        fig = plot_metrics(metrics=self.metrics)
        self.save_figure(figure=fig, fig_name="metrics_global.png")

        fig = plot_sales_evol(df=self.eval_demand)
        self.save_figure(figure=fig, fig_name="sales_evol.png")


    def save_figure(self, figure: plt.Figure, fig_name: str):
        """
        Save a matplotlib figure
        """
        # Get path
        dst = Dashboard.APP / Dashboard.PATH_STATIC / f"{fig_name}"
        SERVICE.log.info(f"Saving figure {fig_name} under {dst}")
        SERVICE.fs.write(
            figure,
            dst,
            fmt="figure",
        )
