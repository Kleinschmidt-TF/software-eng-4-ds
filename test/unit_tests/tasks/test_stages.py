"""Unit tests for the src.tasks.stages module"""


from src.tasks.stages import Stage
from src.services.filesystem.container import Container


def test_stage_init():
    """Tests the basic Stage attributes"""
    for index, stage_name in enumerate(Stage.STAGES):
        stage = Container.get_stage(stage=stage_name)
        assert hasattr(
            stage, "index"), "Stage should have an 'index' attribute"
        assert stage.index == index, f"Index of Stage {stage_name} should be {index}"


def test_stage_comparison():
    """Tests logical tests on Stage instances"""
    index_before = 0
    index_after = 1

    stage_before = Container.get_stage(stage=Stage.STAGES[index_before])
    stage_after = Container.get_stage(stage=Stage.STAGES[index_after])

    assert stage_before <= stage_after, f"Stage {stage_before.name} should be <= Stage {stage_after.name}"
    assert stage_before < stage_after, f"Stage {stage_before.name} should be < Stage {stage_after.name}"
    assert not stage_before == stage_after, f"Stage {stage_before.name} should not be == Stage {stage_after.name}"
    assert not stage_before >= stage_after, f"Stage {stage_before.name} should not be >= Stage {stage_after.name}"
    assert not stage_before > stage_after, f"Stage {stage_before.name} should not be > Stage {stage_after.name}"


def test_stage_validity():
    """Tests if the 'is_valid' method of Stage behaves appropriately"""
    for stage_name in Stage.STAGES:
        assert Stage.is_valid_stage(
            stage_name), f"Stage {stage_name} should be valid"
