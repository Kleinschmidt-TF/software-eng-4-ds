"""
This modules evaluate demand predictions
"""

import pandas as pd

from src.context.prediction_context import PredictionContext
from src.data.data_fetch.data import DataProcess
from src.demand_forecast.processing.data_pipeline import DataPipeline
from src.demand_forecast.processing.feature_engineering import FeatureEng, Map, Agg
from src.services.filesystem.scenario import Scenario
from src.services.service_provider import ServiceProviderHandler
from src.services.constant.fields import Fields
from src.tasks.stages import Stage
from src.utils.func_utils import transform_date
from .dashboard import Dashboard
from .utils import Metrics

SERVICE = ServiceProviderHandler()


class Evaluation:
    """
    Class aiming to evaluate demand prediction. Must be run after demand forecast
    """

    input_data = [
        DataProcess(name="demand_predictions",
                    data_granularity={"products": {Fields.PRODUCT_ID: Map(column=Fields.PRODUCT_ID)},
                                      "location": {Fields.STORE_ID: Map(column=Fields.STORE_ID)},
                                      "time": {"week": Map(column=Fields.WEEK)}},
                    granularity=SERVICE.config.demand_forecast.granularity),
        DataProcess(name=Fields.TRANSACTION_TABLE,
                    data_granularity={"products": {Fields.PRODUCT_ID: Map(column=Fields.PRODUCT_ID)},
                                      "location": {Fields.STORE_ID: Map(column=Fields.STORE_ID)},
                                      "time": {
                                          "week": Agg(
                                              func=transform_date,
                                              agg="sum", column=Fields.WEEK, init_column="date"),
                                          "day": Agg(
                                              func=transform_date,
                                              agg="sum", column=Fields.WEEK,
                                              init_column=Fields.DATE)}},
                    granularity=SERVICE.config.demand_forecast.granularity)]

    def __init__(self, pred_context: PredictionContext) -> None:
        super().__init__()

        # Inputs
        self.context = pred_context

        self.granularity = SERVICE.config.demand_forecast.granularity

        self.evaluation_pipeline = None

        # Dashboard
        self.dashboard = None

    def evaluate(self, scenario, generate_report: bool = True) -> None:
        """
        Method to evaluate demand forecast by comparing it to historical data

        :param scenario: input scenario of the run
        :param generate_report: boolean whether dashborad needs to be created
        :return:
        """
        SERVICE.log.info(f"Evaluating demand prediction")

        self.evaluation_pipeline = DataPipeline(context=self.context, scenario=scenario,
                                                scope="evaluation")

        self.evaluation_pipeline.input_data = self.input_data

        self.evaluation_pipeline.granularity = self.granularity

        self.evaluation_pipeline.pipeline = [
            DataPipeline.Feature(
                id="predictions",
                data_name="demand_predictions",
                load={"start": "information_horizon", "end": "end_date"},
                scope=["evaluation"]
            ),
            DataPipeline.Feature(
                id="actuals",
                data_name=Fields.TRANSACTION_TABLE,
                load={"start": "information_horizon", "end": "end_date"},
                transformer={"transformers": [{"transformer": FeatureEng.rename,
                                               "col": Fields.NB_SOLD_PIECES,
                                               "new_col": "demand_act"},
                                              {"transformer": FeatureEng.manage_nan_features,
                                               "strategy": SERVICE.config.demand_forecast.nan_strategy},
                                              ], "type": "series"},
                scope=["evaluation"]
            ),
        ]

        self.evaluation_pipeline.index = {"data": "predictions", "from": "feature"}

        trained_data, evaluation_data = self.evaluation_pipeline.run(scope="evaluation")

        metrics = Metrics(evaluation_data)

        # Save DataFrame with actual and predictions
        self.save_data(data=evaluation_data, scenario=scenario)

        # Create dashboard and generate it
        self.dashboard = Dashboard(eval_demand=evaluation_data, metrics=metrics)
        if generate_report:
            self.dashboard.create_dashboard()

        bias = str(round(metrics.bias, 2))
        smape = str(round(metrics.smape, 2))

        SERVICE.log.info(f"Evaluation finished")
        SERVICE.log.info(f"""
        ---------------------------------------
        Number of products : {len(self.context.products()["products"]) if self.context.products()[
            "products"] else "All"}
        Number of stores : 
        {len(self.context.location()["location"]) if self.context.location()["location"] else "All"}
        Evaluation metrics :
         - Bias : {bias}%
         - Smape : {smape}%
        """)

        scenario.output["Bias"] = bias
        scenario.output["Smape"] = smape

    def save_data(self, data: pd.DataFrame, scenario: Scenario):
        """
        Save evaluation DataFrame
        """
        # Define path to save predictions
        fmt = "csv"
        dst = scenario.DEMAND_BACKTEST
        dst = scenario.relpath(path=dst, stage=Stage.PREDICTION_BACKTESTED)
        # Save data
        SERVICE.log.info(f"Saving demand backtest data under {dst}")
        SERVICE.fs.write(
            data,
            dst,
            fmt=fmt,
            index=False,
        )
