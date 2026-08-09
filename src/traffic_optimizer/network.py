from dataclasses import dataclass, field

from .intersection import Intersection
from .road import Road


@dataclass
class CityNetwork:
    intersections: dict[str, Intersection] = field(default_factory=dict)
    roads: dict[str, Road] = field(default_factory=dict)

    def add_intersection(self, intersection: Intersection) -> None:
        if intersection.id in self.intersections:
            raise ValueError(f"Intersection '{intersection.id}' already exists.")

        self.intersections[intersection.id] = intersection

    def add_road(self, road: Road) -> None:
        if road.id in self.roads:
            raise ValueError(f"Road '{road.id}' already exists.")

        if road.source not in self.intersections:
            raise ValueError(f"Source intersection '{road.source}' does not exist.")

        if road.destination not in self.intersections:
            raise ValueError(
                f"Destination intersection '{road.destination}' does not exist."
            )

        self.roads[road.id] = road
