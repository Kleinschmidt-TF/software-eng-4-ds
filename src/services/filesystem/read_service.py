"""
This script contains service to read files
"""

import pickle
from typing import Any

import pandas as pd
import yaml


class DataReadService:
    """
    Service aiming to read files
    """

    @staticmethod
    def _read_df(func, src: str, **kwargs) -> pd.DataFrame:
        """
        Main method to read files from distinct format
        """
        return func(src, **kwargs)

    @staticmethod
    def csv(src: str, **kwargs) -> pd.DataFrame:
        """
        Read csv file

        :param src: path where the file is stored
        :param kwargs: other parameters to read file with
        :return: DataFrame with data loaded
        """

        return DataReadService._read_df(func=pd.read_csv, src=src, **kwargs)

    @staticmethod
    def pickle(src: str, **kwargs) -> Any:
        """
        Read pickle object

        :param src: path where the object is saved
        :param kwargs: other parameters to be passed to `pickle.load`
        :return: Object stores under src
        """

        with open(src, "rb") as _file:
            data = pickle.load(_file, **kwargs)
        return data

    @staticmethod
    def yaml(src: str, **kwargs) -> dict:
        """
        Read yaml object

        :param src: path where the object is saved
        :param kwargs: other parameters to be passed to `yaml.load`
        :return: Object stores under src
        """
        with open(src, "r") as info:
            yaml_dict = yaml.safe_load(info)
        return yaml_dict

    @staticmethod
    def sql(src: str, **kwargs):
        """
        Read sql query

        :param src: path where the object is saved
        :param kwargs: other parameters to be passed to `read()`
        :return: Object stores under src
        """

        with open(src, "r") as file_query:
            query = file_query.read()
        return query
