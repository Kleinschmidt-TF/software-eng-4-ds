import os
import pathlib as pl

import pandas as pd
from jinja2 import Template

from src.data.mock_data.seed import seed_tables
from src.demand_forecast.processing.feature_engineering import Agg
from src.services.service_provider import ServiceProviderHandler
from src.tasks.stages import Stage
from src.utils.func_utils import get_init_column, get_index_from_granularity

SERVICE = ServiceProviderHandler()


class DataProcess:
    """
    Class to manage Data object.
    """

    def __init__(self, name: str, data_granularity: dict, granularity: dict, data=None):
        self.name = name
        self.data_granularity = data_granularity
        self.granularity = granularity
        self.index_names = [self.data_granularity[granularity][self.granularity[granularity]['value']].column for
                            granularity in self.data_granularity.keys() if
                            self.granularity[granularity]['value'] is not None]
        self.data_features = None
        self._data = data

        # Check if the chosen granularity is implemented
        for gran, value in get_index_from_granularity(self.granularity).items():
            if gran in self.data_granularity.keys():
                if value not in self.data_granularity[gran].keys():
                    raise NotImplementedError(
                        f"{value} granularity has not been implemented for data {name}")


    def fetch_data(self, context, dst: str, fmt: str = "csv") -> pd.DataFrame:
        """
        Get transactions DataFrame
        :param context: contains information to retrieve data
        :param dst: destination path to write
        :param fmt: writing format
        :return: transactions DataFrame filtered
        """

        # Create table if not exist
        seed_tables()

        # Load query
        # Get query path
        path_query = pl.Path(__file__).resolve().parent / "queries" / f"query_{self.name}.sql"
        query = SERVICE.fs.read(dst=path_query, fmt=path_query.suffix[1:])

        # Fill query with parameters
        query_args = {}
        for granularity in self.granularity:
            kwargs = {}
            if granularity == "time":
                kwargs = {"start": context.start_date, "end": context.end_date}
            query_args.update(getattr(context, granularity)(**kwargs))

        query_to_run = Template(query).render(**query_args).strip()
        SERVICE.log.debug(f"Running query \n{query_to_run}")

        # Run query
        data = SERVICE.db.read(sql=query_to_run)
        SERVICE.log.debug(f"Data loaded, shape is {data.shape}")

        # Clean data
        SERVICE.log.debug("Cleaning data")
        if "time" in self.data_granularity.keys() and "date" in get_init_column(self.data_granularity):
            data["date"] = pd.to_datetime(data["date"])

        SERVICE.fs.write(
            data,
            dst,
            fmt=fmt,
            index=False,
        )

        return data

    def load(self, context=None, scenario=None, start=None, end=None, scope=None, fmt: str = "csv", **kwargs):

        """
        Get DataFrame :
        If the input data is not in the scenario folder or the provided is  different from the last context,
        It fetches the data from the sql database

        :param context: input context that contains information to retrieve data
        :param scenario: input scenario of the run
        :param start: start date of the specific data frame
        :param end: end date of the specific dataframe
        :param scope: training, prediction or evaluation
        :param fmt: format of the saved dataframe

        :return input dataframe (pd.DataFrame)

        When the data are fetched, the time horizon is the widest as possible
        """
        if self._data is None:

            stage_fetched, dst, need_to_be_fetched = self.is_input_file_exists(scope=scope, scenario=scenario,
                                                                               context=context, file_name=self.name,
                                                                               strict=False)

            if need_to_be_fetched:
                SERVICE.log.info(f"Fetching {self.name} data")

                data = self.fetch_data(
                    context=context, dst=dst, fmt=fmt
                )
                SERVICE.log.info(
                    f"Saved {self.name} under {dst}, scenario={str(scenario)}, stage={stage_fetched}")


            else:
                if "time" in self.data_granularity.keys() and "date" in get_init_column(self.data_granularity):
                    date_parser_args = {
                        "parse_dates": ["date"],
                        "date_parser": lambda x: pd.datetime.strptime(x, "%Y-%m-%d")}
                else:
                    date_parser_args = {}

                SERVICE.log.info(
                    f"Loading {self.name} from {dst}, scenario={str(scenario)}, stage={stage_fetched}")
                data = SERVICE.fs.read(
                    dst,
                    fmt=fmt,
                    **kwargs,
                    **date_parser_args
                )

            if "time" in self.data_granularity.keys() and "date" in get_init_column(self.data_granularity):
                data = data[(data.date <= getattr(context, end)) & (data.date >= getattr(context, start))]

            return data
        else:
            return self._data

    def aggregate(self, df, context):
        """
        Aggregate based on index and granularity of the data
        :param df: input dataframe
        :param context: context of the step
        :return: output dataframe aggregated
        """

        # 1. get data feature names (not index) before aggregation
        data_all_index = get_init_column(self.data_granularity, all=True)
        data_features = [feature_column for feature_column in df.columns if feature_column not in set(data_all_index)]

        # 2. Aggregate if the specific index has Agg method transformation
        for granularity, gran_value in get_index_from_granularity(granularity=self.granularity).items():

            if granularity in self.data_granularity.keys():
                granularity_item = self.data_granularity[granularity][gran_value]

                if isinstance(granularity_item, Agg):
                    df[granularity_item.column] = granularity_item.func(df=df, init_column=granularity_item.init_column,
                                                                        context=context,
                                                                        granularity=self.granularity[granularity][
                                                                            'value'])
                    df = df.drop(columns=[granularity_item.init_column])
                    df = df.groupby(self.index_names, as_index=False)[data_features].agg(
                        granularity_item.agg)

        return df

    def transformer(self, df, transformer, **kwargs):
        """Run transformer method"""
        return transformer(data=df, **kwargs)

    def filter(self, df, func, level):
        """Run filter method"""
        df = func(df, level)

        return df

    @staticmethod
    def is_input_file_exists(scope, scenario, context, file_name, fmt: str = "csv", strict: bool = True):
        """Check if file needs to be fetched"""
        if scope == "training":
            stage_fetched = Stage.TRAINING_FETCHED
        elif scope == "prediction":
            stage_fetched = Stage.PREDICTION_FETCHED
        elif scope == "evaluation":
            stage_fetched = Stage.PREDICTION_BACKTESTINGFETCHED
        else:
            raise ValueError(f"scope {scope} unknown")

        # If the context of the scenario has changed, fetch again the data.
        data_context_path = scenario.relpath(path=context.file_name, stage=context.file_name_stage)
        if os.path.isfile(data_context_path):
            data_context = context.__class__.load(src=data_context_path)
        else:
            data_context = {}

        dst = scenario.relpath(path=file_name + "." + fmt, stage=stage_fetched)

        # It needs to be fetched if the file doesn't exist or the context is different
        if data_context:
            need_to_be_fetched = not SERVICE.fs.exists(dst) or (
                    data_context.data != context.data and SERVICE.fs.exists(dst) and strict)
        # or the context file doesn't exist
        else:
            need_to_be_fetched = True

        return stage_fetched, dst, need_to_be_fetched
