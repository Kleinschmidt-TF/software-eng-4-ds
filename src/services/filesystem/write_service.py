"""
This script contains service to write files
"""

import pickle
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import yaml


class DataWriteService:
    """
    Service aiming to write files
    """

    @staticmethod
    def _write_df(func_name: str, df: pd.DataFrame, dst: str, **kwargs):
        """
        Main method to write file of distinct format
        """
        # Write DataFrame, getting pandas method
        getattr(df, func_name)(dst, **kwargs)

    @staticmethod
    def csv(df: pd.DataFrame, dst: str, **kwargs) -> None:
        """
        Write csv file

        :param df: DataFrame to be saved
        :param dst: destination path to save DataFrame
        :param kwargs: parameters to be passed to save function
        """
        return DataWriteService._write_df("to_csv", df=df, dst=dst, **kwargs)

    @staticmethod
    def pickle(obj: Any, dst: str, **kwargs) -> None:
        """
        Write pickle object

        :param obj: any serializable object
        :param dst: destination path to save object
        :param kwargs: parameters to be passed to `pickle.dump`
        """

        with open(dst, "wb") as _file:
            pickle.dump(obj, _file, **kwargs)

    @staticmethod
    def figure(figure: plt.Figure, dst: str) -> None:
        """
        Write matplotlib Figure object

        :param figure: figure object
        :param dst: destination path
        :param kwargs: parameters to be passed to save
        """
        with open(dst, "wb") as _file:
            figure.savefig(_file)

    @staticmethod
    def txt(text: str, dst: str) -> None:
        """
        Write text

        :param text: text to write
        :param dst: destination path
        """
        with open(dst, "w") as _file:
            _file.write(text)

    @staticmethod
    def yaml(dict: dict, dst: str) -> None:
        """
        Write yaml

        :param dict: dict to write
        :param dst: destination path
        """
        with open(dst, "w") as _file:
            yaml.safe_dump(dict, _file, default_flow_style=False)
