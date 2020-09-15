""""
Main script to run test demand forecast pipeline
"""

import importlib
import logging
import pathlib

from src.services.filesystem.scenario import Scenario
from src.services.service_provider import ServiceProviderHandler
from src.tasks.stages import Stage

# 1. Set the log
logging.basicConfig(level=logging.DEBUG)

# 2. Set the config
SERVICE = ServiceProviderHandler()

# 3. Instantiate scenario
scenario_test = Scenario.load(
    scenario_path=pathlib.Path("test") / "data_test" / "demand_prediction")
scenario_to_test = Scenario(input_path="tmp",
                            name="scenario_to_test",
                            config=scenario_test.config)

# 4. Define the pipeline
dfp = importlib.import_module("src.tasks.demand_forecast")

# 5. Define Test pipeline
DEMAND_FORECAST_PIPELINE_TEST = dfp.DemandForecastPipeline(
    scenario=scenario_to_test,
    scenario_test=scenario_test,
    begin_stage=scenario_to_test.stage,
    final_stage=Stage.PREDICTION_BACKTESTED,
    test=True)

# 6. Run test pipeline
SERVICE.log.info("\033[1mStarting the Test pipeline\033[0m")
DEMAND_FORECAST_PIPELINE_TEST.run()
SERVICE.log.info("\033[1mTest passed !\033[0m")

scenario_to_test.delete(disk=True)
scenario_test.delete(disk=False)
