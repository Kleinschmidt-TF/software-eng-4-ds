"""
This script contains meta class for context instantiation.
A context is an instance containing scope parameters and is specific to training or
prediction
"""

from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from src.services.service_provider import ServiceProviderHandler

SERVICE = ServiceProviderHandler()


class MetaContext(ABC):
    """
    Abstract context for training or prediction. Contains parameters shared between
    these two instances
    """

    __module_name__ = None
    _granularity_dict = granularity_dict = {"day": 7, "week": 1, "month": 0}

    def __init__(self, name=None):

        # Define global parameters
        self._name = name
        self._is_training = None
        self._is_backtest = False

        # Define scope parameters
        self._start_date = None
        self._end_date = None
        self._information_horizon = None
        self.location_value = SERVICE.config.demand_forecast[name].location.value
        self.products_value = SERVICE.config.demand_forecast[name].products.value
        self._location = '(' + ','.join(
            map(str, SERVICE.config.demand_forecast[name].location.value)) + \
                         ')' if SERVICE.config.demand_forecast[
                                    name].location.value is not None else None
        self._products = '(' + ','.join(
            map(str, SERVICE.config.demand_forecast[name].products.value)) + \
                         ')' if SERVICE.config.demand_forecast[
                                    name].products.value is not None else None
        self._location_granularity = SERVICE.config.demand_forecast[name].location.granularity
        self._products_granularity = SERVICE.config.demand_forecast[name].products.granularity
        self.time_granularity = SERVICE.config.demand_forecast[name].time.granularity

    def __str__(self):
        return self._name

    @property
    def name(self):
        """return name of the context"""
        if self._name is None:
            raise NotImplementedError("Context doesn't have name")
        return self._name

    @property
    def is_training(self):
        """return if is training context (True) or not"""
        if self._is_training is None:
            raise NotImplementedError("Context training state is not defined")
        return self._is_training

    @property
    def start_date(self):
        """return the starting date of the context"""
        if self._start_date is None:
            raise NotImplementedError("Context start date is not defined")
        return self._start_date

    @property
    def end_date(self):
        """return the end date of the context"""
        if self._end_date is None:
            raise NotImplementedError("Context end date is not defined")
        return self._end_date

    @property
    def information_horizon(self):
        """Return the information horizon, last date of known information"""
        return self._information_horizon

    @property
    def clip_date(self):
        """return clip data if backtest is off"""
        if self.is_backtest:
            return None
        return pd.to_datetime(SERVICE.config.run_info.information_horizon)

    def location(self) -> dict:
        """Return the name of location granularity and its value. It is used for the sql request"""
        return {"location_name": self._location_granularity, "location": self._location}

    def products(self) -> dict:
        """Return the name of product granularity and its value. It is used for the sql request"""
        return {"products_name": self._products_granularity, "products": self._products}

    def time(self, start, end) -> dict:
        """Return the name of time granularity and its value. Basically used for the sql request"""
        return {"time_name": self.time_granularity,
                "start_date": datetime.strftime(start, "%Y-%m-%d"),
                "end_date": datetime.strftime(end, "%Y-%m-%d")}

    @property
    def is_backtest(self) -> bool:
        """Boolean which returns true whether the run mode is in backtesting"""
        return self._is_backtest

    def save(self, stage, scenario) -> None:
        """save context in a yaml file """
        fmt = "yaml"
        name = self._name + "." + fmt
        dst = scenario.relpath(path=name, stage=stage)
        dict_to_save = self.__dict__.copy()
        for key, value in dict_to_save.items():
            if type(value) == pd.Timestamp:
                dict_to_save[key] = value._short_repr
        SERVICE.fs.write(dict_to_save, dst=dst, fmt=fmt, )

    @classmethod
    def load(cls, src):
        """load context from the yaml file"""
        context = cls()
        context.__dict__.update(SERVICE.fs.read(dst=src, fmt="yaml"))
        for key, value in context.__dict__.items():
            if key in ["_end_date", "_start_date", "_information_horizon"]:
                context.__dict__[key] = pd.to_datetime(value, format="%Y-%m-%d")
            if key == "location_value" and isinstance(value, list):
                context.__dict__[key] = tuple(value)
        return context

    @property
    def data(self) -> dict:
        """return context data as a dictionary"""
        return self.__dict__

    @property
    def file_name(self) -> str:
        """return the file name of the context where it is saved"""
        return self.name + ".yaml"

    def print_summary(self):
        """print summary of the context"""
        SERVICE.log.info(
            f'\n\t {self._name} : \n\t | -----------INPUT----------- | -----------TARGET-----------'
            f' |\n{self._start_date.date()}----------'
            f'{SERVICE.config.demand_forecast.range_week_sales}----------'
            f'{self._information_horizon.date()}----------'
            f'{SERVICE.config.demand_forecast[self._name].time.time_range}'
            f'----------{self._end_date.date()}\n\n Location ID : '
            f'{"All" if self._location is None else self._location}'
            f' \n\n Number of products : '
            f'{"All" if self._products is None else len(self._products)}')

    @abstractmethod
    def time_index(self, granularity):
        """Return time index"""
        raise NotImplementedError

    @abstractmethod
    def file_name_stage(self):
        """return stage where the context is saved"""
        raise NotImplementedError
