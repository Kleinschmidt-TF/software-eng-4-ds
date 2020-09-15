"""Defines the operator class.

An operator is a step in a pipeline, that executes a task, given a configuration, stage and data,
and updates the stage.
Operators have dependencies (on other operators / on the stage)
"""

from src.context.meta import MetaContext
from src.services.service_provider import ServiceProviderHandler
from src.services.filesystem.container import Container
from .stages import Stage

SERVICE = ServiceProviderHandler()


class Operator:
    """
    An operator is a step in a pipeline, that executes a task, given a configuration, stage
    and data, and updates the stage.
    Operators have dependencies. In our case we choose to define dependencies using a stage,
    rather than pairwise dependencies.
    """

    def __init__(self, operator_id: str, final_stage: "Stage", python_callable: callable):
        """Create an Operator.

        :param operator_id: ID of the operator
        :param final_stage: stage that the operator triggers on completion
        :param python_callable: function to use to run the Operator.
            The python_callable should take 3 keyword arguments:
            - stage: a Stage object
            - context: a MetaContext object
            And it should return 2 objects:
            - output_context: a MetaContext object
        """

        self._id = str(operator_id)
        self._python_callable = python_callable

        if isinstance(final_stage, str):
            final_stage = Container.get_stage(stage=final_stage)
        self.final_stage = final_stage

    def __call__(self, stage: "Stage", context: "MetaContext", scenario: "Scenario"):
        """Executes the Operator.

        :param stage: a Stage object
        :param context: a MetaContext object or None

        Returns:
        :returns output_context: the new context
        """

        assert isinstance(stage, Stage)

        with SERVICE.timer(context=str(context), task=self._id):
            output_context = self._python_callable(
                stage=stage,
                context=context,
                scenario=scenario,
            )

        return output_context
