""""
Main script to run demand forecast pipeline
"""

import importlib
import logging

from src.services.filesystem.scenario import Scenario
from src.services.service_provider import ServiceProviderHandler
from src.utils.cli import cli_set_up, cli_read

# 1. Set the log
logging.basicConfig(level=logging.DEBUG)

# 2. Set the Service
SERVICE = ServiceProviderHandler()

# 3. Set up the CLI
parser = cli_set_up()

# 4. Read the CLI
scenario_path, scenario_name, final_stage = cli_read(parser=parser)

# 5. Instantiate scenario
if scenario_path is not None:
    scenario = Scenario.load(scenario_path=scenario_path)
else:
    scenario = Scenario(input_path="./tmp", name=scenario_name, config=SERVICE.config)

# 6. Define the pipeline
dfp = importlib.import_module("src.tasks.demand_forecast")
DEMAND_FORECAST_PIPELINE = dfp.DemandForecastPipeline(
    scenario=scenario,
    begin_stage=scenario.stage,
    final_stage=final_stage,
    test=False)

# 7. Run pipeline
SERVICE.log.info("\033[1mStarting the pipeline\033[0m")
DEMAND_FORECAST_PIPELINE.run()
SERVICE.log.info("\033[1mMy job here is done\033[0m")
scenario.delete(disk=False)
