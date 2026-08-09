from dataclasses import dataclass
from enum import Enum


class ControlType(str, Enum):
    SIGNAL = "signal"
    ROUNDABOUT = "roundabout"
    STOP = "stop"


@dataclass
class Approach:
    lanes: int = 1
    left_turn_lane: bool = False
    right_turn_lane: bool = False
    bike_lane: bool = False

    def __post_init__(self) -> None:
        if self.lanes < 1:
            raise ValueError("An approach must have at least one lane.")


@dataclass
class Intersection:
    id: str
    control_type: ControlType

    north: Approach
    south: Approach
    east: Approach
    west: Approach

    pedestrian_crossings: bool = True
