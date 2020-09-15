"""
Defines the demand forecast Pipeline instance

NB: although the Operators output a context and data,
we would need too much refactoring to really make use of that;
moreover everything is handled by the Scenario (and file system),
so each Operator callable returns None as data
"""

from src.backtest.evaluate import Evaluation
from src.context.prediction_context import PredictionContext
from src.context.training_context import TrainingContext
from src.demand_forecast.demand_forecast import DemandForecast
from src.demand_forecast.processing.data_pipeline import DataPipeline
from src.services.filesystem.scenario import Scenario
from src.services.service_provider import ServiceProviderHandler
from .operators import Operator
from .pipeline import Pipeline
from .stages import Stage

SERVICE = ServiceProviderHandler()


# Training
def fetch_training_data(scenario=None, stage=None, context=None):
    """Callable to fetch the training data"""
    train_context = TrainingContext()
    SERVICE.log.info("\033[1mFetching training data\033[0m")
    DataPipeline.fetch_data(DemandForecast.input_data, scope="training", context=train_context, scenario=scenario)
    train_context.print_summary()
    return train_context


FETCH_TRAINING_DATA_OPERATOR = Operator(
    "Fetches training data",
    final_stage=Stage.TRAINING_FETCHED,
    python_callable=fetch_training_data,
)


def train_demand(scenario=None, stage=None, context=None):
    """Callable to train the DemandForecast model and save it"""
    assert isinstance(context, TrainingContext)
    SERVICE.log.info("\033[1mTraining demand model\033[0m")
    demand_forecast = DemandForecast()
    demand_forecast.fit(train_context=context, scenario=scenario)
    context.save(stage=context.file_name_stage, scenario=scenario)
    demand_forecast.save_cls(scenario=scenario)
    return context


TRAIN_DEMAND_OPERATOR = Operator(
    "Trains Demand",
    final_stage=Stage.TRAINING_TRAINED,
    python_callable=train_demand,
)


# Predictions
def fetch_prediction_data(scenario=None, stage=None, context=None):
    """Callable to fetch prediction data"""
    pred_context = PredictionContext()
    SERVICE.log.info("\033[1mFetching prediction data\033[0m")
    DataPipeline.fetch_data(DemandForecast.input_data, scope="prediction", context=context, scenario=scenario)
    pred_context.print_summary()
    return pred_context


FETCH_PREDICTION_DATA_OPERATOR = Operator(
    "Fetches prediction data",
    final_stage=Stage.PREDICTION_FETCHED,
    python_callable=fetch_prediction_data,
)


def predict_demand(scenario=None, stage=None, context: "PredictionContext" = None):
    """Callable to predict demand with trained model"""
    assert isinstance(context, PredictionContext)
    SERVICE.log.info("\033[1mPredicting demand\033[0m")
    demand_forecast = DemandForecast.load_cls(context=TrainingContext, scenario=scenario)
    predictions = demand_forecast.predict(prediction_context=context, scenario=scenario)
    demand_forecast.save_predictions(df=predictions, scenario=scenario)
    context.save(stage=context.file_name_stage, scenario=scenario)
    return context


PREDICT_DEMAND_OPERATOR = Operator(
    "Predicts demand",
    final_stage=Stage.PREDICTION_PREDICTED,
    python_callable=predict_demand,
)


# Evaluation of predictions
def fetch_backtest_data(scenario=None, stage=None, context: "PredictionContext" = None):
    """Callable to fetch backtest data"""
    src = scenario.relpath(path=PredictionContext.file_name, stage=Stage.PREDICTION_FETCHED)
    pred_context = PredictionContext.load(src=src)
    SERVICE.log.info("\033[1mFetching backtest data\033[0m")
    DataPipeline.fetch_data(Evaluation.input_data, scope="evaluation", context=context, scenario=scenario)
    return pred_context


FETCH_BACKTEST_DATA_OPERATOR = Operator(
    "Fetches backtesting data",
    final_stage=Stage.PREDICTION_BACKTESTINGFETCHED,
    python_callable=fetch_backtest_data,
)


def evaluate(scenario=None, stage=None, context=None):
    """Callable to evaluate prediction"""
    assert isinstance(context, PredictionContext)
    SERVICE.log.info("\033[1mEvaluating predictions\033[0m")
    evaluation = Evaluation(pred_context=context)
    evaluation.evaluate(scenario=scenario)
    return context


EVALUATE_OPERATOR = Operator(
    "Evaluates prediction",
    final_stage=Stage.PREDICTION_BACKTESTED,
    python_callable=evaluate,
)


class DemandForecastPipeline(Pipeline):
    """Pipeline to run demand forecast model training / prediction / evaluation

    Extension of the Pipeline class, with pre-defined operators
    """

    def __init__(
            self,
            scenario: "Scenario",
            scenario_test: "Scenario" = None,
            begin_stage: str = Stage.TRAINING_INIT,
            final_stage: str = Stage.PREDICTION_BACKTESTED,
            test: bool = False,
    ):
        operators = [
            FETCH_TRAINING_DATA_OPERATOR,
            TRAIN_DEMAND_OPERATOR,
            FETCH_PREDICTION_DATA_OPERATOR,
            PREDICT_DEMAND_OPERATOR,
            EVALUATE_OPERATOR,
        ]

        super(DemandForecastPipeline, self).__init__(
            scenario=scenario,
            scenario_test=scenario_test,
            begin_stage=begin_stage,
            final_stage=final_stage,
            test=test,
            operators=operators,
        )
