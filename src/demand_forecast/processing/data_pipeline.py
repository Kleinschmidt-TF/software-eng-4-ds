from collections import namedtuple
from functools import reduce
from typing import Union

import pandas as pd

from src.context.meta import MetaContext
from src.services.service_provider import ServiceProviderHandler
from src.utils.func_utils import get_index_from_granularity

SERVICE = ServiceProviderHandler()


class DataPipeline:
    """
    Class to handle the data pipeline.
    this class is defined on four main properties : index, pipeline, input_data and granularity
    """

    Feature = namedtuple("Feature", "id data_name load aggregate transformer filter merge scope")
    Feature.__new__.__defaults__ = ("-", "-", {}, {}, {}, {}, {}, [])

    def __init__(self, scenario, context, scope):

        """
        Initialize the data pipeline with the current scenario the current context
        and set None the four main properies
        :param scenario: current scenario of the run
        :param context:  current context of the run
        """
        self.scenario = scenario
        self._context = context
        self.from_index = None
        self.index_names = []
        self._granularity = None
        self._input_data = {}
        self._pipeline = None
        self._index = None
        self.scope = scope

    @property
    def granularity(self) -> dict:
        """return granularity o f the pipeline"""
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        """set the granularity of the pipeline"""
        self._granularity = granularity

    @property
    def input_data(self) -> dict:
        """return the input data of the pipeline"""
        return self._input_data

    @input_data.setter
    def input_data(self, input_data: list):
        """set the input data dictionary with data_name: Data object"""
        self._input_data = {data.name: data for data in input_data}

    @property
    def index(self) -> Union[str, pd.DataFrame]:
        """
        The index can come from directly from:

            - the feature (when 'from_index'=='feature'). It means that the index doesn't
              need to be created but it will be directly the index of the Object data corresponding
              to the index_data

            - the data (when 'from_index'=='data'). It means that the index needs to be created with
              the specific input data (index_data). If multiple sources of data are provided, the
              index is built as all combination of all different index values.

        :return:
        """
        if self.from_index == "feature":
            return f"Index in {self._index}"

        index_series = []
        for gran, index in self._index.items():
            if gran in list(get_index_from_granularity(self.granularity).keys()):
                trained_data, df, index_names = self.run_step(context=self._context,
                                                              feature=index,
                                                              scope=self.scope)
                index_series.append(df[index_names])
        return reduce(
            lambda a, b: a.eval("key=1").merge(b.eval("key=1"), on="key", how="inner").drop(
                ["key"], axis=1),
            index_series)

    @index.setter
    def index(self, index: dict):
        """
        The index can come from directly from:

            1. the feature (when `'from_index'=='feature'`). It means that the index doesn't
               need to be created but it will be directly the index of the Object data corresponding
                to the index_data.
            2. the data (when `'from_index'=='data'`). It means that the index needs to be created
               with the specific input data (index_data).

        Here, the `from_index` and the `index_data` (either the name if the input Data object,
        either the name of the input Feature object) is stored
        """

        index_data = index['data']
        from_index = index['from']

        for gran, index_ in get_index_from_granularity(self.granularity).items():
            data = self._input_data[index_data[gran].data_name] if from_index == "data" else \
                self._input_data[
                    list(filter(lambda x: x.id == index_data, self.pipeline))[0].data_name]
            assert index_ in list(data.data_granularity[gran].keys()) \
                , "Missing index in index definition"
            self.index_names.append(data.data_granularity[gran][index_].column)

        self._index = index_data
        self.from_index = from_index

    @property
    def pipeline(self):
        """return the list of feature engineering steps of the pipeline"""
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        """set the feature engineering step of the pipeline"""
        self._pipeline = pipeline

    def run(self, scope: str, trained_data: dict = None):
        """
        Function to run each feature engineering step oif the pipeline including the creation of
        the index if it is necessary.

        1. Set the index
           If the index comes from the feature no specific changes, if the index comes from external
           data than the feature, create it.

        2. Run the feature engineering step
           For each feature engineering step, run the function 'run_step" that will load, transform
           a specific dataframe

        3. Merge to the current dataframe
           Merge based on the index of the pipeline and the index of the Data object of the feature.

        :param scope: "training", "prediction" or "evaluation" (str)
        :param trained_data:  dictionary with the trained data of feature engineering step when
               there is a training transformation (i.e OneHotEncoding).
        :return: trained_data and output dataframe with all features
        """
        required_property = self._granularity and self._input_data and self._index and self._pipeline
        if all(required_property):

            if self.from_index == "data":
                final_df = self.index.copy()
                pipeline = self.pipeline
            elif self.from_index == "feature":
                pipeline = list(filter(lambda x: x.id != self._index, self._pipeline))
                index = list(filter(lambda x: x.id == self._index, self._pipeline))[0]
                trained_data, final_df, index_names = self.run_step(context=self._context,
                                                                    feature=index, scope=scope,
                                                                    trained_data=trained_data)
            else:
                raise NotImplementedError

            for feature in pipeline:
                if scope in feature.scope:
                    trained_data, df, index_names = self.run_step(context=self._context,
                                                                  feature=feature, scope=scope,
                                                                  trained_data=trained_data)
                    final_df = final_df.merge(df, **feature.merge,
                                              on=list(
                                                  set(self.index_names).intersection(index_names)))

                # assert len(
                # data) == len_data_check, 'the number of rows has changed after feature adding'
            return trained_data, final_df

        else:
            raise NotImplementedError(
                f"{[prop for prop in required_property if prop is None]} has not been implemented")

    def run_step(self, context: MetaContext, feature: Feature, scope: str = None,
                 trained_data: dict = None):
        """

        The run a processing step. It means run each method of the feature object if it is not None:
            1. load
            2. aggregate
            3. transform
            4. filter

        The transform method is not straightforward :
            Two kinds of transform method:
                1. trained transformer (when `transf['trained']` is True. It means the Feature
                   engineering method will be fitted on the data
                2. Otherwise (when `transf['trained']` is False. It means the feature engineering
                   method won't be fitted on the data

            Two kinds of transformation process:
                1. `series`. It means all transformation will be perform in series, (sequentially)
                2. `parallel`. It means that all transformation will be perform in parallel so from
                    the same starting data frame

        :param context: context of the run
        :param feature: feature is a Feature object from DataPipeline class
        :param scope: scope of the run (either "training", "prediction", "evaluation"
        :param trained_data: data dictionary with the trained data from feature engineering steps
        :return:
        """
        # 1 . get Data object
        data = self.input_data[feature.data_name]

        # 2. Load data
        if feature.load:
            df = data.load(scenario=self.scenario, context=context, scope=self.scope,
                           **feature.load)

        # 3. Aggregate data
        df = data.aggregate(df=df, context=context)  # mandatory step

        # 4. Remove undesirable features
        if data.name in SERVICE.config.demand_forecast.features.keys():
            features = SERVICE.config.demand_forecast.features[data.name]
            if len(features) > 0:
                df = df[data.index_names + list(features)]

        # 5. Transform the data frame with feature engineering methods
        if feature.transformer:
            if feature.transformer["type"] == "series":
                for transf_ in feature.transformer["transformers"]:
                    if "trained" in transf_.keys():
                        if transf_["trained"] and scope == "training":
                            output_trained_data, df = \
                                data.transformer(df=df,
                                                 is_training=context.is_training,
                                                 **transf_)
                            trained_data[transf_["transformer"].__name__] = output_trained_data
                        elif transf_["trained"] and scope == "prediction":
                            df = data.transformer(df=df, is_training=context.is_training,
                                                  trained_data=trained_data[
                                                      transf_["transformer"].__name__], **transf_)
                    else:
                        df = data.transformer(df=df, **transf_)
            elif feature.transformer["type"] == "parallel":
                df_partial_list = [data.transformer(df=df, **transf_) for transf_ in
                                   feature.transformer["transformers"]]
                df = reduce(lambda left, right: pd.merge(left, right, on=list(
                    set(data.index_names).intersection(left.columns).intersection(right.columns))),
                            df_partial_list)
            else:
                raise ValueError("Unknown type for transformer")

        # 6. filter it
        if feature.filter:
            df = data.filter(df=df, **feature.filter)

        return trained_data, df, list(set(data.index_names).intersection(df.columns))

    @staticmethod
    def fetch_data(input_data, scope: str, context, scenario) -> None:
        """
        Fetch input data from sql database
        :param input_data: input data o fthe pipeline
        :param scope scope of the pipeline (training, prediction or evaluation)
        :param context, context of the pipeline
        :param scenario, current scenario of the pipeline
        :return: None
        """
        for input_data_ in input_data:
            stage_fetched, dst, need_fetching = \
                input_data_.is_input_file_exists(scope=scope,
                                                 context=context,
                                                 scenario=scenario,
                                                 file_name=input_data_.name)
            if need_fetching:
                input_data_.fetch_data(context=context, dst=dst)
