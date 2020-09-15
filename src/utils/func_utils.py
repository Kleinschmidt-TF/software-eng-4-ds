"""
This script contains useful function used in pipeline
"""

import pathlib as pl

import pandas as pd
import yaml

from src.services.constant.fields import Fields
from src.services.service_provider import ServiceProviderHandler

SERVICE = ServiceProviderHandler()


def get_categorical_value(row: pd.Series, col_names: list) -> str:
    """
    Useful function to get initial value for columns encoded
    """
    for col in col_names:
        if row[col] == 1:
            return col
    return "<unknown>"


def filter_target(data: pd.DataFrame, level) -> pd.DataFrame:
    """
    Filter DataFrame with filters specified in config
    :param data: input dataframe
    :param level: threshold of the target filter
    """
    SERVICE.log.info(
        f"Filtering training set with filters specified in config : "
        f"min_sales={level}"
    )

    # Aggregating at product level
    df = data.groupby([Fields.PRODUCT_ID], as_index=False)[
        SERVICE.config.demand_forecast.target].agg("sum")
    bad_products = list(
        df.loc[df[SERVICE.config.demand_forecast.target] < level][Fields.PRODUCT_ID]
    )
    SERVICE.log.info(
        f"Dropping {len(bad_products)} products : {bad_products}")

    # Filter data and update scope
    data = data.loc[~(data[Fields.PRODUCT_ID].isin(bad_products))]
    SERVICE.log.info(
        f"Shape after filtering : {data.shape}, it corresponds "
        f"to {data[Fields.PRODUCT_ID].nunique()} products"
    )
    return data


def transform_date(df: pd.DataFrame, init_column: str, context, granularity) -> pd.Series:
    """
    function to convert date column to week index or day index during aggregation
    :param df: input_dataframe
    :param init_column: initial date column (datetime format)
    :param context: current context of the run
    :param granularity: granularity of the input data
    :return: Pd.Series with new date aggregation
    """
    if granularity == "week":
        return ((df[init_column] - context.information_horizon).dt.days - 1) // 7 + 1
    elif granularity == "day":
        return ((df[init_column] - context.information_horizon).dt.days + 1)
    else:
        raise NotImplementedError("Not implemented")


def get_index_from_granularity(granularity: dict) -> dict:
    """
    From granularity dictionary, get the granularity by index if it is not None
    :param granularity: granularity dictionary
    :return: output dictionary of the granularity by index
    """
    return {granularity_: value['value'] for granularity_, value in granularity.items()
            if value['value'] is not None}


def get_init_column(data_granularity: dict, all: bool = False) -> list:
    """
    From data_granularity, get the initial column of the data index
    :param data_granularity: dictionary of the granularity of a Data object
    :params all: if it includes all granularity
    :return: list of initial column name of the index
    """
    from src.demand_forecast.processing.feature_engineering import Agg
    index_init_column = []
    for gran, data_gran in data_granularity.items():
        granularity = SERVICE.config.demand_forecast.granularity
        for value in data_gran.values():
            if granularity[gran]['value'] is not None or all:
                if isinstance(value, Agg):
                    index_init_column.append(value.init_column)
                else:
                    index_init_column.append(value.column)
    return index_init_column


def check_type(data_: str):
    """
    Check if a dataframe has a the right type from type.yml
    """

    def test_type_(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            with open(pl.Path(__file__).resolve().parents[1] / "data" / "data_fetch" / "type.yml") \
                    as f:
                data_type = yaml.load(f, Loader=yaml.SafeLoader)
            for column in data_type[data_].keys():
                assert column in data.columns, f"column {column} is not in the data : {data_}"
                assert data[column].dtype == data_type[data_][
                    column], f"column {column} has a wrong type. it should be " \
                    f"{data_type[data_][column]} instead of {data[column].dtype} in {data_}"
            return data

        return wrapper

    return test_type_
