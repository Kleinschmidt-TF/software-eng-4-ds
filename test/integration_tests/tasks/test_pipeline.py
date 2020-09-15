"""
Integration tests for the src.tasks.pipeline module

This is an integration test because it tests the interaction between modules
"""

import unittest.mock as mock

from src.tasks.pipeline import Pipeline
from src.tasks.operators import Operator
from src.tasks.stages import Stage


def test_pipeline_init():
    """Tests that a Pipeline can be correctly setup"""

    pipeline = Pipeline(
        scenario=None,
        begin_stage=Stage.STAGES[0],
        final_stage=Stage.STAGES[-1],
        operators=[],
    )
    assert isinstance(pipeline.begin_stage,
                      Stage), "Pipeline.begin_stage should be a Stage"
    assert isinstance(pipeline.final_stage,
                      Stage), "Pipeline.final_stage should be a Stage"

    assert pipeline.begin_stage < pipeline.final_stage, "Pipeline begin_stage should be < final_stage"


@mock.patch.object(Operator, "__call__")
def test_pipeline_run(operator_call):
    """Tests if a Pipeline runs an Operator accordingly"""
    operator = Operator(
        operator_id="test_operator",
        final_stage=Stage.STAGES[1],
        python_callable=mock.MagicMock(),
    )

    pipeline = Pipeline(
        scenario=mock.MagicMock(),
        begin_stage=Stage.STAGES[0],
        final_stage=Stage.STAGES[1],
        operators=[operator],
    )
    pipeline.run()

    n_calls = len(operator_call.mock_calls)
    assert n_calls == 1, f"Operator should be called once, got {n_calls} calls"
    assert pipeline.current_stage == pipeline.final_stage, f"Pipeline should be at its final stage"
