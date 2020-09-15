"""
This script contains class for training context.
"""



import pandas as pd

from src.services.service_provider import ServiceProviderHandler
from src.tasks.stages import Stage
from .meta import MetaContext

SERVICE = ServiceProviderHandler()


class TrainingContext(MetaContext):
    """
    Training context containing scope parameters training specific

    Defines: _locations, _start_date (datetime.datetime), _end_date (datetime.datetime)
    as  well as Time scope (from config values) as follows:
        - information_horizon = run_info.information_horizon - 7 * demand_forecast.training_scope.time_range

        - start_date = _information_horizon - 7 * demand_forecast.range_week_sales - 1

        - end_date = _information_horizon + 7 * demand_forecast.prediction_scope.time_range
    """
    __module_name__ = "training_context"

    def __init__(self):
        super().__init__(TrainingContext.__module_name__)

        # Define global parameters
        self._is_training = True
        self._information_horizon = (
            pd.to_datetime(SERVICE.config.run_info.information_horizon) -
            pd.to_timedelta(
                7 * SERVICE.config.demand_forecast.training_context.time.time_range, unit="days"
            )
        )

        # Define scope parameters
        self._start_date = self._information_horizon - pd.to_timedelta(
            7 * SERVICE.config.demand_forecast.range_week_sales - 1, unit="days"
        )
        self._end_date = self._information_horizon + pd.to_timedelta(
            7 * SERVICE.config.demand_forecast.training_context.time.time_range, unit="days"
        )

    def time_index(self, granularity):
        return range(
            1, (SERVICE.config.demand_forecast.training_context.range_week_sales + 1) * self._granularity_dict[
                granularity])

    @property
    def file_name_stage(self):
        return Stage.TRAINING_TRAINED
