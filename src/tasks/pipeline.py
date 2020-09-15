"""
Define Pipeline class.

A Pipeline is a set of tasks (Operators) organized with dependencies.
Running a Pipeline will execute the Operators according to their dependencies.

Here, dependencies are linear and linked to stages: the Pipeline starts from a begin_stage,
then executes each Operator and moves to the next stage.

A Pipeline run in test mode will trigger a check of the Operator's output against a reference
Scenario.
"""

import collections

from src.services.filesystem.scenario import Scenario
from src.services.service_provider import ServiceProviderHandler
from src.services.filesystem.container import Container
from .stages import Stage

log = ServiceProviderHandler().log


class Pipeline(collections.Iterable):
    """
    A Pipeline is a set of tasks (Operators) organized with dependencies.
    Running a Pipeline will execute the Operators according to their dependencies.
    """

    def __init__(
            self,
            scenario: "Scenario",
            scenario_test: "Scenario" = None,
            begin_stage: str = None,
            final_stage: str = None,
            test: bool = False,
            operators: list = None,
    ):
        """
        Init for pipeline.
        """
        operators = operators or []

        # Convert stages passed to the Pipeline to Stage objects
        if isinstance(begin_stage, str):
            begin_stage = Container.get_stage(stage=begin_stage)
        assert isinstance(
            begin_stage,
            Stage), f"begin_stage parameter {begin_stage} should be a str or Stage object"

        if isinstance(final_stage, str):
            final_stage = Container.get_stage(stage=final_stage)
        assert isinstance(
            final_stage,
            Stage), f"final_stage parameter {final_stage} should be a str or Stage object"

        self.scenario = scenario
        self.scenario_test = scenario_test
        self.begin_stage = begin_stage
        self.final_stage = final_stage
        self.current_stage = begin_stage
        self._operators = operators
        self._test = test

    def __iter__(self):
        """Iterates through the operators"""
        for operator in self._operators:
            yield operator

    def __len__(self):
        """Returns the number of operators"""
        return len(self._operators)

    @property
    def test(self):
        return self._test

    def run(self, input_context=None):
        """Runs the pipeline from its begin Stage to its final Stage

        :param input_context: MetaContext or None, context to start the Pipeline

        Each Operator is run sequentially.
        If the current Pipeline stage is at or above an Operators' final stage, this stage
        is skipped input_context is passed as 'context' kwarg.
        Output_context (output of the Operator call) is used as the next Operators' context
        (if not None) after each Operator is executed, the current_stage is updated to match the
        Operators' final_stage. If the Pipeline runs in test mode, the Scenario & ScenarioTest are
        compared at the current_stage.

        Stops when the Pipeline's final_stage is reached or when the last Operator is run.
        """

        self.current_stage = self.begin_stage

        # Loop through operators
        for operator in self:

            # Do not execute if we are at or above the operator final stage
            if self.current_stage >= operator.final_stage:
                log.info(
                    f"{operator._id} final stage already reached, going to next operator")
                continue

            # Execute the operator, gather results
            output_context = operator(
                scenario=self.scenario,
                stage=self.current_stage,
                context=input_context,
            )

            # If necessary, test the result
            if self.test:
                self.scenario.test = False
                self.scenario.compare(
                    stage=operator.final_stage,
                    scenario=self.scenario_test,
                )

            # Update/save the scenario
            self.scenario.stage = operator.final_stage.name
            self.scenario.save_info()
            if self.test:
                self.scenario.test = True

            # Increment the stage
            self.current_stage = operator.final_stage
            if self.current_stage >= self.final_stage:
                log.info("Reached Pipeline final stage")
                break

            # This operator's outputs are the next one's inputs
            if output_context is not None:
                input_context = output_context

        self.scenario.save()