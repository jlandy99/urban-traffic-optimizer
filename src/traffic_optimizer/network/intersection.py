from dataclasses import dataclass, field
from enum import Enum


class IntersectionType(str, Enum):
    SIGNAL = "signal"
    ROUNDABOUT = "roundabout"
    STOP = "stop_controlled"


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
    row: int
    col: int
    intersection_type: IntersectionType

    north: Approach = field(default_factory=lambda: Approach())
    south: Approach = field(default_factory=lambda: Approach())
    east: Approach = field(default_factory=lambda: Approach())
    west: Approach = field(default_factory=lambda: Approach())

    pedestrian_crossings: bool = True

    def to_dict(self) -> dict:
        return {
            "row": self.row,
            "col": self.col,
            "type": self.intersection_type,
        }

    def __str__(self) -> str:
        symbols = {
            "signal": "S",
            "roundabout": "R",
            "stop_controlled": "T",
        }

        return symbols.get(self.intersection_type, "?")
