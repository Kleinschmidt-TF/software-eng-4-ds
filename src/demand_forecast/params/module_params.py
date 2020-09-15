"""
This script contains demand forecast module parameters
"""

from box import Box

from src.services.service_provider import ServiceProviderHandler

SERVICE = ServiceProviderHandler()

class DemandParams:
    """
    Class containing demand module parameters
    """

    def __init__(self):
        super().__init__()

        # Module parameters
        self.target = SERVICE.config.demand_forecast.target
        self.granularity = SERVICE.config.demand_forecast.granularity

        # Model parameters
        self._model_name = SERVICE.config.demand_forecast.model.name
        self._model_params = SERVICE.config.demand_forecast.model.params

        # Features parameters
        self._features = SERVICE.config.demand_forecast.features
        self._range_week_sales = SERVICE.config.demand_forecast.range_week_sales

        # Processing parameters
        self._nan_strategy = SERVICE.config.demand_forecast.nan_strategy
        self._min_sales = SERVICE.config.demand_forecast.training_context.min_sales

    @property
    def model_name(self) -> str:
        """return model name"""
        if not isinstance(self._model_name, str):
            raise NotImplementedError("model name must be set in config")
        return self._model_name

    @property
    def model_params(self) -> Box:
        """return model parameters"""
        if not isinstance(self._model_params, Box):
            raise NotImplementedError("model params must be set in config")
        return self._model_params

    @property
    def features(self) -> dict:
        """return feature dictionary"""
        if not isinstance(self._features, dict):
            raise NotImplementedError("features must be set in config")
        return self._features

    @property
    def range_week_sales(self) -> int:
        """return the range week sales"""
        if not isinstance(self._range_week_sales, int):
            raise NotImplementedError("range_week_sales must be set in config")
        return self._range_week_sales

    @property
    def nan_strategy(self) -> str:
        """return the nan strategy"""
        if not isinstance(self._nan_strategy, str):
            raise NotImplementedError("nan strategy must be set in config")
        return self._nan_strategy

    @property
    def min_sales(self) -> int:
        """return the minimum of sales to filter the target"""
        if not isinstance(self._min_sales, int):
            SERVICE.log.warning("min sales params is not specified, set it to 0")
            return 0
        return self._min_sales
