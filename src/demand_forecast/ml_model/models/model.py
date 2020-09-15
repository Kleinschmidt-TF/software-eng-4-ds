"""
This script contains tree based demand machine learning models
"""

from abc import ABC, abstractmethod

import pandas as pd
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor


class MetaModel(ABC):
    """
    Main class to train a tree based ML model
    """
    __module_name__ = None

    @classmethod
    def __init_subclass__(cls):
        super.__init_subclass__()
        setattr(MetaModel, cls.__module_name__, cls)


    @abstractmethod
    def fit(self, x_train: pd.DataFrame, target: pd.Series):
        """
        Fit method
        :param x_train: training data
        :param target: target data
        :return:
        """
        raise RuntimeError('Not implemented')

    @abstractmethod
    def predict(self, x_pred: pd.DataFrame) -> pd.Series:
        """
        Predict method
        :param x_pred: input data
        :return: prediction data
        """
        raise RuntimeError('Not implemented')


class RandomForestDemandModel(RandomForestRegressor, MetaModel):
    """
        Model from sklearn.ensemble.RandomForestRegressor

        Name in configuration : random_forest
    """

    __module_name__ = "random_forest"


class ExtraTreeDemandModel(ExtraTreesRegressor, MetaModel):
    """
        Model from sklearn.ensemble.ExtraTreesRegressor

        Name in configuration : extra_tree
    """
    __module_name__ = "extra_tree"


class XGBoostDemandModel(XGBRegressor, MetaModel):
    """
        Model from sklearn.ensemble.ExtraTreesRegressor

        Name in configuration : xgboost
    """

    __module_name__ = "xgboost"
