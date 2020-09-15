"""
This script contains script to process features and
"""

from collections import namedtuple
from typing import Optional, Tuple

import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.services.service_provider import ServiceProviderHandler

SERVICE = ServiceProviderHandler()


class FeatureEng:
    """
    Class to handle feature engineering functions

    Those functions are generally called during the data pipeline by the transform function
    """

    @staticmethod
    def normalize_data(
            data: pd.DataFrame,
            scaler: Optional[StandardScaler] = None,
            not_scale: Optional[list] = None,
            with_mean: Optional[bool] = True,
            with_std: Optional[bool] = True
    ) -> Tuple[pd.DataFrame, StandardScaler]:
        """
        Scaling DataFrame features

        :param data: DataFrame containing features to be scaled
        :param scaler: object used to scale data, use it when present
        :param not_scale: columns which should not be scaled
        :param with_mean: to center data
        :param with_std: to standardize data
        :return: Scaled DataFrame and object used to scale data
        """
        # We split into data to scale and data to not scale
        data_not_scale = data[not_scale] if not_scale else data[[]]
        data_to_scale = data.drop(not_scale, axis=1)
        col_names = list(data_to_scale.columns)
        # If scaler is not available, it means it has to be fitted
        if not scaler:
            scaler = StandardScaler(with_mean=with_mean, with_std=with_std)
            data_to_scale = scaler.fit_transform(data_to_scale)
        else:
            data_to_scale = scaler.transform(data_to_scale)

        # Concatenate scaled data and not scaled data
        data = pd.concat([
            pd.DataFrame(data_to_scale, columns=col_names),
            data_not_scale
        ], axis=1)
        return data, scaler

    @staticmethod
    def encode_data(
            data: pd.DataFrame, is_training: bool, trained: str,
            trained_data: Optional[dict] = None,
    ) -> Tuple[dict, pd.DataFrame]:
        """
        Encode categorical columns

        :param data: DataFrame containing columns to be encoded
        :param is_training: bool true whether if the run is at the training step
        :param trained_data:  LabelEncoder dictionary containing column and labels encoded
        :return: DataFrame with encoded columns and dictionary with labels for each column and
                 LabelEncoder dictionary if the run is at training step.
        """

        SERVICE.log.info(f"Encoding features")

        if is_training:
            assert trained_data is None, \
                "Fitting categorical encoding, 'trained_data' should be None"
            cat_cols = list(data.select_dtypes(include=['category', 'object']).columns)
            train = True
            trained_data = {}
        else:
            assert trained_data is not None, \
                "Encoding categorical variable needs an input 'trained_data' dictionary"
            cat_cols = trained_data.keys()
            train = False

        for column in cat_cols:
            try:
                encoded_col = pd.get_dummies(data[column], prefix=column)
                if train:
                    SERVICE.log.info(f"Fitting categorical features encoding")
                    trained_data[column] = list(encoded_col.columns)
                else:
                    # Deal with unknown classes
                    SERVICE.log.info(f"Encoding categorical features")
                    encoded_col = encoded_col.reindex(columns=trained_data[column], fill_value=0)

                data = (
                    pd.concat([data, encoded_col.rename(
                        columns=lambda col: col.strip().replace(" ", ""))], axis=1)
                        .drop([column], axis=1)
                )
            except Exception as e:
                raise ArithmeticError(f"Could not encode column {column} : {e}")
        if train:
            return trained_data, data

        return data

    @staticmethod
    def pivot_values(
            data: pd.DataFrame, index: list, col: list, agg: str) -> pd.DataFrame:
        """
        From a DataFrame containing a variable at article x daily level, pivot table and
        aggregate it at weekly level

        :param df: DataFrame at article x daily level containing values to be aggregated
        :param add_avg: boolean indicating if average features has to be computed

        :return: DataFrame at article level with column for each week
        """

        df = data.groupby(index)[col].agg(agg).unstack(level=-1, fill_value=0).reset_index()
        df.columns = ['%s%s' % (a, '_%s' % b if b != '' else '') for a, b in df.columns]

        return df

    @staticmethod
    def agg_value(data: pd.DataFrame, index: list, col: list, agg: str) -> pd.DataFrame:
        """

        :param data: input dataframe
        :param index: index on which the groupby is applied
        :param col: aggregation column
        :param agg: type of aggregation, i.e sum, median, mean, ...
        :return: Output dataframe with aggregated columns
        """

        data = data.groupby(index)[col].agg(agg).reset_index()
        data = data.rename(columns={col_: col_ + "_" + agg for col_ in col})
        return data

    @staticmethod
    def manage_nan_features(data: pd.DataFrame, strategy) -> pd.DataFrame:
        """
        Manage NaN features
        """
        SERVICE.log.info(
            f"Managing NaN features with strategy {strategy}")
        if strategy == "strict":
            assert not data.isnull().values.any(), "Values should not be NaN"
        else:
            raise ValueError(
                f"nan_strategy value is not handled : {strategy}"
            )

        return data

    @staticmethod
    def rename(data: pd.DataFrame, col: str, new_col: str) -> pd.DataFrame:
        """
        Rename dataframe column
        :param data: input dataframe
        :param col: initial column name
        :param new_col: new column name
        :return: Output Dataframe
        """
        data = data.rename(columns={col: new_col})
        return data


Map = namedtuple("Map", "column")
Agg = namedtuple("Agg", "func agg init_column column")
