"""Defines stages of a run. Stages are defined sequentially and are specific to the demand forecast
use case.

The Stage class defines the sequence of stages.
The Stage class defines methods on a Stage (comparison, incrementation).
"""
import pathlib as pl

class ReachedLastStage(LookupError):
    """Exception raised when we try to increment the Stage,
    but the last Stage is reached.
    """


def stage_comparison(comparison):
    """Wrapper to force comparison methods on two Stage instances"""

    def new_comparison(stage, other):
        assert isinstance(
            other, Stage), "Can only compare a Stage with a str or another Stage"
        return comparison(stage, other)

    return new_comparison

class Stage:
    """Defines a stage of the run. It can be incremented.

    Stage objects can also be compared (is the current Stage prior to another one?)
    """

    TRAINING_INIT = "TRAINING_INIT"
    TRAINING_FETCHED = "TRAINING_FETCHED"
    TRAINING_PREPROCESSED = "TRAINING_PREPROCESSED"
    TRAINING_TRAINED = "TRAINING_TRAINED"
    PREDICTION_INIT = "PREDICTION_INIT"
    PREDICTION_FETCHED = "PREDICTION_FETCHED"
    PREDICTION_PREPROCESSED = "PREDICTION_PREPROCESSED"
    PREDICTION_PREDICTED = "PREDICTION_PREDICTED"
    PREDICTION_BACKTESTINGFETCHED = "PREDICTION_BACKTESTINGFETCHED"
    PREDICTION_BACKTESTED = "PREDICTION_BACKTESTED"

    STAGES = [
        TRAINING_INIT,
        TRAINING_FETCHED,
        TRAINING_PREPROCESSED,
        TRAINING_TRAINED,
        PREDICTION_INIT,
        PREDICTION_FETCHED,
        PREDICTION_PREPROCESSED,
        PREDICTION_PREDICTED,
        PREDICTION_BACKTESTINGFETCHED,
        PREDICTION_BACKTESTED,
    ]

    @classmethod
    def is_valid_stage(cls, stage):
        """Checks if the stage is valid"""
        if isinstance(stage, str):
            return stage in cls.STAGES
        elif isinstance(stage, Stage):
            return stage.name in cls.STAGES
        else:
            raise AttributeError(f"{stage} fomat unknown")

    def __init__(self, name: str = None, parent: str= None, children: list=None):
        """Initializes a Stage.
        """
        # Name-defined stage: check the name using Stage
        assert Stage.is_valid_stage(
            name), f"Stage name {name} not valid, use one of {Stage.STAGES}"

        self.index = Stage.STAGES.index(name)
        self.name = name
        self.parent = parent
        self.children = children
        self.path = pl.Path(parent) / name

    @stage_comparison
    def __eq__(self, other):
        return (self.index == other.index) & (self.name == other.name)

    @stage_comparison
    def __ge__(self, other):
        return self.index >= other.index

    @stage_comparison
    def __le__(self, other):
        return self.index <= other.index

    @stage_comparison
    def __gt__(self, other):
        return self.index > other.index

    @stage_comparison
    def __lt__(self, other):
        return self.index < other.index

    def __str__(self):
        return self.name

    def increment(self):
        """Increments the Stage object: passes to the next Stage defined by Stage"""
        new_index = self.index + 1
        if new_index <= len(self.STAGES) - 1:
            self.index = new_index
            self.name = self.STAGES[self.index]
        else:
            raise ReachedLastStage(
                f"Stage {self.name} ({self.index}) is the last stage")
