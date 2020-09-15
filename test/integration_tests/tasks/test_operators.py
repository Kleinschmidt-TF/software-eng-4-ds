"""Unit tests for the src.tasks.operators module"""


from unittest import mock

from src.tasks.operators import Operator
from src.tasks.stages import Stage
from src.services.filesystem.container import Container

BEGIN_STAGE = Container.get_stage(stage=Stage.STAGES[0])
FINAL_STAGE = Container.get_stage(stage=Stage.STAGES[1])


def test_operator_init():
    """Tests the Operator setup & ID"""
    operator_id = "test_operator"

    operator = Operator(
        operator_id=operator_id,
        final_stage=FINAL_STAGE,
        python_callable=None,
    )
    assert operator._id == operator_id, "Incorrect ID"


@mock.patch("src.tasks.stages.Stage")
def test_operator_call(mock_stage):
    """Tests an Operator call"""
    mock_callable = mock.MagicMock()
    mock_callable.return_value = "return_context"

    operator_id = "test_operator"

    operator = Operator(
        operator_id=operator_id,
        final_stage=FINAL_STAGE,
        python_callable=mock_callable,
    )

    res = operator(
        stage=BEGIN_STAGE,
        context=None,
        scenario=None,
    )
    assert len(
        mock_callable.mock_calls) == 1, f"python_callable should be called once"
    assert res == "return_context", "Incorrect return value"
