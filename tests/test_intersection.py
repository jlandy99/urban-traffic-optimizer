import pytest
from traffic_optimizer.intersection import Approach, ControlType, Intersection


def test_create_signalized_intersection():
    intersection = Intersection(
        id="I_0",
        control_type=ControlType.SIGNAL,
        north=Approach(lanes=2, left_turn_lane=True),
        south=Approach(lanes=2, left_turn_lane=True),
        east=Approach(lanes=2),
        west=Approach(lanes=2),
    )

    assert intersection.id == "I_0"
    assert intersection.control_type == ControlType.SIGNAL
    assert intersection.north.lanes == 2
    assert intersection.north.left_turn_lane is True
    assert intersection.pedestrian_crossings is True


def test_approach_requires_positive_lanes():
    with pytest.raises(ValueError):
        Approach(lanes=0)
