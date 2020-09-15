"""
Script containing main demand forecast module to perform training and prediction
"""

from typing import Tuple, Optional

import pandas as pd

from src.context.meta import MetaContext
from src.context.prediction_context import PredictionContext
from src.context.training_context import TrainingContext
from src.data.data_fetch.data import DataProcess
from src.demand_forecast.processing.data_pipeline import DataPipeline
from src.services.filesystem.scenario import Scenario
from src.services.constant.fields import Fields
from src.services.service_provider import ServiceProviderHandler
from src.tasks.stages import Stage
from src.utils.func_utils import filter_target, transform_date
from .ml_model.demand_ml_model import DemandMLModel
from .params.module_params import DemandParams
from .processing.feature_engineering import FeatureEng, Map, Agg

SERVICE = ServiceProviderHandler()


class DemandForecast:
    """
    Class defining main demand forecast allowing training and prediction
    """
    __module_name__ = "demand"

    # Define input data for the processing pipeline
    # For each input data and for each index, different granularity definition can be set up
    input_data = [
        DataProcess(
            name=Fields.TRANSACTION_TABLE,
            data_granularity={"products": {Fields.PRODUCT_ID: Map(column=Fields.PRODUCT_ID)},
                              "location": {Fields.STORE_ID: Map(column=Fields.STORE_ID)},
                              "time": {"week": Agg(
                                  func=transform_date,
                                  agg="sum", column=Fields.WEEK, init_column=Fields.DATE),
                                  "day": Agg(
                                      func=transform_date,
                                      agg="sum", column=Fields.WEEK, init_column=Fields.DATE)}},
            granularity=SERVICE.config.demand_forecast.granularity),
        DataProcess(
            name=Fields.PRODUCT_TABLE,
            data_granularity={"products": {Fields.PRODUCT_ID: Map(column=Fields.PRODUCT_ID)}},
            granularity=SERVICE.config.demand_forecast.granularity),
    ]

    def __init__(self):

        # Define module parameters
        self.params = DemandParams()
        self.trained_data = {}

        # Instantiate demand forecast machine learning chosen among factory
        self.ml_model = DemandMLModel(
            name=self.params.model_name, params=self.params.model_params
        )

        # Define granularity for the model
        self.granularity = SERVICE.config.demand_forecast.granularity

    @property
    def pipeline(self):
        """
        Define data processing pipeline
        :return: List of Feature engineering steps for the training and the prediction

        Note :
            - `data_name` correspond to the name of one of the input data
            - `scope` params in DataPipeline.Feature allows to know if the feature is for training,
               prediction or both.
            - `transformer` perform one of the feature engineering function on the dataframe.
              If multiple transformers are applied. `type` parameter indicates if the processing
              has to be in series or in parallel.
              If `trained` is one of the transformer parameter, it means that the transformer has to
              be fit on the data (i.e OneHotEncoding).

        """

        return [

            DataPipeline.Feature(
                id="target",
                data_name="transactions",
                load={"start": "information_horizon", "end": "end_date"},
                filter={"func": filter_target, "level": self.params.min_sales},
                scope=["training"]

            ),
            DataPipeline.Feature(
                id="product_features",
                data_name=Fields.PRODUCT_TABLE,
                load={"start": "start_date", "end": "information_horizon"},
                transformer={"transformers": [{"transformer": FeatureEng.encode_data,
                                               "trained": True},
                                              {"transformer": FeatureEng.manage_nan_features,
                                               "strategy": self.params.nan_strategy},
                                              ], "type": "series"},
                scope=["training", "prediction"]

            ),
            DataPipeline.Feature(
                id="sales_features",
                data_name=Fields.TRANSACTION_TABLE,
                load={"start": "start_date", "end": "information_horizon"},
                transformer={"transformers": [{"transformer": FeatureEng.pivot_values,
                                               "index": [Fields.PRODUCT_ID, Fields.WEEK],
                                               "col": [Fields.NB_SOLD_PIECES],
                                               "agg": "sum"},
                                              {"transformer": FeatureEng.agg_value,
                                               "index": [Fields.PRODUCT_ID],
                                               "col": [Fields.NB_SOLD_PIECES],
                                               "agg": "sum"}],
                             "type": "parallel"},
                scope=["training", "prediction"]
            )
        ]

    def fit(self, train_context: TrainingContext, scenario: Scenario) -> None:
        """
        Main method to train demand forecast pipeline

        :param train_context: context of the training containing scope information
        :param scenario: input scenario
        """
        SERVICE.log.info(f"Training demand module")

        # 1. Set training pipeline
        training_pipeline = DataPipeline(scenario=scenario, context=train_context, scope="training")

        # 2. Set granularity of the processing
        training_pipeline.granularity = self.granularity

        # 3. Set input data
        training_pipeline.input_data = self.input_data

        # 4. Set pipeline (feature engineering steps)
        training_pipeline.pipeline = self.pipeline

        # 5. Set index of the data pipeline
        training_pipeline.index = {"data": "target", "from": "feature"}

        # 6. Run the data processing pipeline
        self.trained_data, data_train = training_pipeline.run(scope="training",
                                                              trained_data=self.trained_data)

        # 7. Save prediction data
        self.save_data(data=data_train, scenario=scenario, context=train_context)

        # 8. Split training data
        _, x_train, y_train = self.split_dataset(data=data_train,
                                                 index=training_pipeline.index_names,
                                                 context=train_context)

        # 9. Train model
        self.ml_model.fit(x_train, y_train)

    def predict(self, prediction_context: PredictionContext, scenario: "Scenario") -> pd.DataFrame:
        """
        Main method to predict demand with previously trained model

        :param pred_context: context of the prediction containing scope information
        :param scenario: input scenario of the run
        :return: DataFrame containing demand prediction
        """
        SERVICE.log.info(f"Predicting with demand module")

        # 0. Check that ML model is already fitted
        assert self.ml_model.is_fitted, "Demand ML model is not yet fitted"

        # 1. Set prediction data pipeline
        prediction_pipeline = DataPipeline(scenario=scenario, context=prediction_context,
                                           scope="prediction")

        # 2. Set granularity of the data pipeline
        prediction_pipeline.granularity = self.granularity

        # 3. Add new input data required for the prediction index
        self.input_data += [
            DataProcess(
                name="time_index",
                data_granularity={"time": {"week": Map(column=Fields.WEEK)}},
                granularity=self.granularity,
                data=pd.DataFrame(data=prediction_context.time_index(
                    self.granularity["time"]["value"]),
                    columns=[Fields.WEEK])),
            DataProcess(
                name="location_index",
                data_granularity={"location": {Fields.STORE_ID: Map(column=Fields.STORE_ID)}},
                granularity=self.granularity,
                data=pd.DataFrame(data=prediction_context.location_value, columns=[Fields.STORE_ID]))]

        # 4. Set input data for the prediction pipeline
        prediction_pipeline.input_data = self.input_data

        # 5. Set feature engineering steps for the prediction
        prediction_pipeline.pipeline = self.pipeline

        # 6. Set the index for the data processing pipeline
        prediction_pipeline.index = {"data": {"products": DataPipeline.Feature(
            id="product_index",
            data_name=Fields.PRODUCT_TABLE,
            load={"start": "information_horizon", "end": "end_date"},
            scope=["prediction"]
        ), "location": DataPipeline.Feature(
            id="location_index",
            data_name="location_index",
            load={"start": "information_horizon", "end": "end_date"},
            scope=["prediction"]
        ), "time": DataPipeline.Feature(
            id="time_index",
            data_name="time_index",
            load={"start": "information_horizon", "end": "end_date"},
            scope=["prediction"]
        )}, "from": "data"}

        # 7. Run the data processing pipeline
        self.trained_data, data_pred = prediction_pipeline.run(scope="prediction",
                                                               trained_data=self.trained_data)

        # 8. Split prediction data
        x_scope, x_pred = self.split_dataset(data=data_pred, index=prediction_pipeline.index_names,
                                             context=prediction_context)

        # 9. Save prediction data
        self.save_data(data=data_pred, context=prediction_context, scenario=scenario)

        # 10. Predict demand
        predictions = self.ml_model.predict(x_pred)
        df_demand = pd.concat(
            [x_scope, pd.DataFrame({"demand": predictions})], axis=1
        )

        # 11. Sanity check
        self._sanity_check(prediction_pipeline=prediction_pipeline, prediction=df_demand)

        return df_demand

    @staticmethod
    def split_dataset(
            data: pd.DataFrame, index: list, context: MetaContext
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.Series]]:
        """
        Split whole DataFrame in scope, features and target
        """
        SERVICE.log.info(
            f"Splitting DataFrame into scope, features and target")
        # Getting scope
        scope = data[index].copy()
        # Getting target in training mode
        if isinstance(context, PredictionContext):
            try:
                target = data.pop(SERVICE.config.demand_forecast.target)
            except KeyError:
                pass
        else:
            target = data.pop(SERVICE.config.demand_forecast.target)

        features = data.drop([Fields.PRODUCT_ID], axis=1)

        if isinstance(context, TrainingContext):
            return scope, features, target

        return scope, features

    @staticmethod
    def _sanity_check(
            prediction_pipeline, prediction: pd.DataFrame) -> None:
        """
        Perform some checks on data
        """
        pipeline_index = prediction_pipeline.index

        # Check shape are identical
        assert prediction.shape[0] == pipeline_index.shape[0], (
            f"shape is not the same : demand {prediction.shape[0]}, "
            f"scope {pipeline_index.shape[0]}"
        )

        # Check products
        for index_name in prediction_pipeline.index_names:
            assert set(prediction[index_name]) == set(pipeline_index[index_name]), (
                f"{index_name} set is not the sames : demand {prediction[index_name].nunique()},"
                f"scope {pipeline_index[index_name].nunique()}"
            )

        SERVICE.log.info(f"Sanity check passed !")

    def save_cls(self, scenario: Scenario) -> None:
        """Save module class"""

        # Define module path
        fmt = "pickle"
        dst = scenario.DEMAND_MODEL
        # Write module
        SERVICE.log.info(
            f"Saving {self.__class__.__name__} module under {dst}")
        stage = Stage.TRAINING_TRAINED
        dst = scenario.relpath(path=dst, stage=stage)
        # Write the model - neither the ServiceProvider attributes nor the context
        SERVICE.fs.write(
            self,
            dst,
            fmt=fmt,
        )

    @classmethod
    def load_cls(cls, context: "TrainingContext", scenario: Scenario) -> "DemandForecast":
        """Load module class"""

        if cls.__module_name__ is None:
            raise TypeError(f"{cls.__name__}.__module_name__ must be set.")

        # Define module path
        fmt = "pickle"
        file_name = scenario.DEMAND_MODEL

        # Load module

        SERVICE.log.info(f"Loading {cls.__name__} module from {file_name}")
        stage = Stage.TRAINING_TRAINED

        src = scenario.relpath(path=file_name, stage=stage)

        # obj = cls()
        obj = SERVICE.fs.read(
            src,
            fmt=fmt,
        )

        obj.context = context

        return obj

    # Methods to save and load predictions

    def save_predictions(self, df: pd.DataFrame, scenario: "Scenario") -> None:
        """Save DataFrame as csv file"""
        # Define path to save predictions
        fmt = "csv"
        dst = scenario.DEMAND_PREDICTION

        # Save data
        SERVICE.log.info(
            f"Saving {self.__class__.__name__} predictions under {dst}")

        dst_path = scenario.relpath(path=dst, stage=Stage.PREDICTION_PREDICTED)
        SERVICE.fs.write(
            df,
            dst_path,
            fmt=fmt,
            index=False,
        )

        # Needed for the backtesting
        if SERVICE.config.run_info.run_mode == "backtest":
            dst_path = scenario.relpath(path=dst, stage=Stage.PREDICTION_BACKTESTINGFETCHED)
            SERVICE.fs.write(
                df,
                dst_path,
                fmt=fmt,
                index=False,
            )

    @classmethod
    def load_predictions(cls, scenario: "Scenario") -> pd.DataFrame:
        """Load predictions previously saved"""
        # Define path to load predictions
        fmt = "csv"
        file_name = scenario.DEMAND_PREDICTION

        # Load predictions
        srv_prov = ServiceProviderHandler()
        srv_prov.log.info(
            f"Loading {cls.__class__.__name__} predictions at {file_name}")

        src = scenario.relpath(path=file_name, stage=Stage.PREDICTION_PREDICTED)
        return srv_prov.fs.read(
            src,
            fmt=fmt,
        )

    # Methods to save and load features / ML model input
    def save_data(self, data: pd.DataFrame, scenario: "Scenario", context: "MetaContext") -> None:
        """Save features data in training or prediction"""
        # Define path to save data
        fmt = "csv"
        dst = scenario.DATA_INPUT
        stage = (Stage.TRAINING_PREPROCESSED if context.name == 'training_context'
                 else Stage.PREDICTION_PREPROCESSED)

        # Save data
        SERVICE.log.info(
            f"Saving input prediction data for {self.__class__.__name__} under {dst}")
        dst = scenario.relpath(path=dst, stage=stage)

        SERVICE.fs.write(
            data,
            dst,
            fmt=fmt,
            index=False,
        )

    def __delattr__(self, item):
        del self.__dict__[item]
