"""
This script contains class for prediction context.
"""

import pandas as pd

from src.services.service_provider import ServiceProviderHandler
from src.tasks.stages import Stage
from .meta import MetaContext

SERVICE = ServiceProviderHandler()


class PredictionContext(MetaContext):
    """
    Prediction context containing scope parameters prediction specific
    """

    __module_name__ = "prediction_context"

    def __init__(self):
        super().__init__(PredictionContext.__module_name__)

        # Define global parameters
        self._is_training = False
        self._is_backtest = SERVICE.config.run_info.run_mode == "backtest"
        self._information_horizon = pd.to_datetime(
            SERVICE.config.run_info.information_horizon
        )

        # Define scope parameters
        self._start_date = self.information_horizon - pd.to_timedelta(
            7 * SERVICE.config.demand_forecast.range_week_sales - 1, unit="days"
        )
        self._end_date = self.information_horizon + pd.to_timedelta(
            7 * SERVICE.config.demand_forecast.prediction_context.time.time_range, unit="days"
        ) if self.is_backtest else None

    def time_index(self, granularity):
        return range(
            1, (SERVICE.config.demand_forecast.prediction_context.time.time_range + 1) * self._granularity_dict[
                granularity])

    @property
    def file_name_stage(self):
        return Stage.PREDICTION_PREDICTED
