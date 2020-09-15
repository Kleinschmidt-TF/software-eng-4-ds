"""
Module to create a standard container object
that is basically a folder outputs
"""
import pathlib as pl
from typing import Union
from shutil import rmtree
from src.tasks.stages import Stage
from src.services.service_provider import ServiceProvider


SERVICE = ServiceProvider()

class Container:

    INFO = "info.yaml"
    CONFIG = "model_config.yaml"
    OUTPUT = "output.yaml"

    # TRAINING & PREDICTION FILES:
    TRAINING = "training"
    PREDICTION = "prediction"

    PRODUCTS = "products.csv"
    TRANSACTIONS = "transactions.csv"
    DATA_INPUT = "data_input.csv"
    DEMAND_MODEL = "demand.pkl"
    TRAINING_CONTEXT = "training_context.yaml"

    DEMAND_PREDICTION = "demand_predictions.csv"
    PREDICTION_CONTEXT = "prediction_context.yaml"

    DEMAND_BACKTEST = "demand_backtest.csv"


    TRAINING_INIT_STAGE = Stage(name=Stage.TRAINING_INIT,
                                parent=TRAINING,
                                children=None)

    TRAINING_FETCHED_STAGE = Stage(name=Stage.TRAINING_FETCHED,
                                   parent=TRAINING,
                                   children=[PRODUCTS,
                                             TRANSACTIONS])

    TRAINING_PREPROCESSED_STAGE = Stage(name=Stage.TRAINING_PREPROCESSED,
                                        parent=TRAINING,
                                        children=[DATA_INPUT])

    TRAINING_TRAINED_STAGE = Stage(name=Stage.TRAINING_TRAINED,
                                   parent=TRAINING,
                                   children=[DEMAND_MODEL,
                                             TRAINING_CONTEXT])

    # PREDICTION FILES:
    PREDICTION_INIT_STAGE = Stage(name=Stage.PREDICTION_INIT,
                                  parent=PREDICTION,
                                  children=None)

    PREDICTION_FETCHED_STAGE = Stage(name=Stage.PREDICTION_FETCHED,
                                     parent=PREDICTION,
                                     children=[PRODUCTS,
                                               TRANSACTIONS])

    PREDICTION_PREPROCESSED_STAGE = Stage(name=Stage.PREDICTION_PREPROCESSED,
                                          parent=PREDICTION,
                                          children=[DATA_INPUT])

    PREDICTION_PREDICTED_STAGE = Stage(name=Stage.PREDICTION_PREDICTED,
                                       parent=PREDICTION,
                                       children=[DEMAND_PREDICTION,
                                                 PREDICTION_CONTEXT])

    PREDICTION_BACKTESTINGFETCHED_STAGE = Stage(
        name=Stage.PREDICTION_BACKTESTINGFETCHED,
        parent=PREDICTION,
        children=[DEMAND_PREDICTION,
                  TRANSACTIONS])

    PREDICTION_BACKTESTED_STAGE = Stage(name=Stage.PREDICTION_BACKTESTED,
                                        parent=PREDICTION,
                                        children=[DEMAND_BACKTEST])

    def __init__(self, location):

        self.build_hierarchy()
        self.storage_location = location

    @classmethod
    def build_hierarchy(cls):

        for stage in cls.stages():
            parent = pl.Path(stage.parent)
            setattr(Container, stage.name, parent / stage.name)
            for file in stage.children:
                setattr(Container,
                        stage.name + "_" + file.split(".")[0].upper(),
                        parent / stage.name / file)

    @classmethod
    def stages(cls):
        stages = []
        for key, stage in vars(cls).items():
            if isinstance(stage, Stage):
                stages.append(stage)

        return stages

    @classmethod
    def get_stage(cls, stage: str):
        if stage in Stage.STAGES:
            return getattr(cls, stage+"_STAGE")

        raise ValueError("Stage : {} not found".format(stage))

    def relpath(self, path: str, stage: Union["Stage",str] = None) -> str:
        """Returns the relative path, depending on the scenario & stage"""
        if isinstance(stage, str):
            stage = self.get_stage(stage=stage)
            os_path = self.storage_location / stage.path / path

        elif isinstance(stage, Stage):
            os_path = self.storage_location / stage.path / path

        else:
            os_path = self.storage_location / path

        return os_path

    def delete(self, disk: bool) -> None:
        """
        Remove the scenario from the memory. If disk is true, it will delete from the disk as well.

        :param disk: bool whether to remove the scenario from the disk

        """
        if disk:
            try:
                rmtree(self.storage_location)
            except FileNotFoundError:
                SERVICE.log('Scenario not found')

        del self