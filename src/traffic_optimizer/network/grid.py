import json
import random
import numpy as np
from dataclasses import dataclass, field
from enum import Enum

from .intersection import Intersection, IntersectionType
from .road import Road


# This enum matches the values of the command line arguments in experiments/run.py
# Do not change unless you also change there, otherwise the simulation functionality will break
class GridMode(int, Enum):
    RANDOM = 1
    ALL_PRIORITY = 2
    ALL_PRIORITY_STOP = 3
    ALL_ALLWAY_STOP = 4
    ALL_TRAFFIC_LIGHT = 5


@dataclass
class Grid:
    rows: int
    cols: int
    intersections: list[Intersection]
    roads: list[Road]
    edge_weights: list[list[float]]
    seed: int | None = None

    def __post_init__(self):
        self.edge_weights = np.ones((self.rows, self.cols))

    def to_dict(self) -> dict:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "seed": self.seed,
            "intersections": [
                intersection.to_dict() for intersection in self.intersections
            ],
            "roads": [
                road.to_dict() for road in self.roads
            ]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self) -> str:
        lookup = {
            (intersection.row, intersection.col): intersection
            for intersection in self.intersections
        }

        lines = []

        for row in range(self.rows):
            cells = []

            for col in range(self.cols):
                cells.append(str(lookup[(row, col)]))

            lines.append("  ".join(cells))

        return "\n".join(lines)


def generate_grid(
    rows: int,
    cols: int,
    seed: int,
    mode: GridMode,
    road_num_lanes: int,
    road_speed_limit_mps: float,
    road_num_lanes_range: tuple[int],
    road_speed_limit_mps_range: tuple[float],
    output_mode: str = "verbose",
) -> Grid:
    if mode == GridMode.ALL_PRIORITY:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.PRIORITY,
            road_num_lanes=road_num_lanes,
            road_speed_limit_mps=road_speed_limit_mps,
            output_mode=output_mode,
        )
    elif mode == GridMode.ALL_PRIORITY_STOP:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.PRIORITY_STOP,
            road_num_lanes=road_num_lanes,
            road_speed_limit_mps=road_speed_limit_mps,
            output_mode=output_mode,
        )
    elif mode == GridMode.ALL_ALLWAY_STOP:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.ALLWAY_STOP,
            road_num_lanes=road_num_lanes,
            road_speed_limit_mps=road_speed_limit_mps,
            output_mode=output_mode,
        )
    elif mode == GridMode.ALL_TRAFFIC_LIGHT:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.TRAFFIC_LIGHT,
            road_num_lanes=road_num_lanes,
            road_speed_limit_mps=road_speed_limit_mps,
            output_mode=output_mode,
        )
    elif mode == GridMode.RANDOM:
        return generate_random_grid(
            rows=rows,
            cols=cols,
            seed=seed,
            road_num_lanes_range=road_num_lanes_range,
            road_speed_limit_mps_range=road_speed_limit_mps_range,
            output_mode=output_mode,
        )


def generate_uniform_grid(
    rows: int,
    cols: int,
    intersection_type: IntersectionType,
    road_num_lanes: int,
    road_speed_limit_mps: float,
    output_mode: str = "verbose",
) -> Grid:
    """
    Generate a uniform grid using a specified intersection type
    """

    intersections = []
    int_id = 0
    for row in range(rows):
        for col in range(cols):
            intersections.append(
                Intersection(
                    id=int_id,
                    row=row,
                    col=col,
                    intersection_type=intersection_type,
                )
            )
            id += 1

    roads = []
    # Horizontal edges
    for i in range(n):
        for j in range(m - 1):
            roads.append(
                Road(
                    id=f"east_{i}_{j}",
                    source=(i, j),
                    destination=(i, j + 1),
                    lanes=road_num_lanes,
                    speed_limit_mps=road_speed_limit_mps,
                )
            )
            roads.append(
                Road(
                    id=f"west_{i}_{j + 1}",
                    source=(i, j + 1),
                    destination=(i, j),
                    lanes=road_num_lanes,
                    speed_limit_mps=road_speed_limit_mps,
                )
            )

    # Vertical edges
    for i in range(n - 1):
        for j in range(m):
            roads.append(
                Road(
                    id=f"south_{i}_{j}",
                    source=(i, j),
                    destination=(i + 1, j),
                    lanes=road_num_lanes,
                    speed_limit_mps=road_speed_limit_mps,
                )
            )
            roads.append(
                Road(
                    id=f"north_{i + 1}_{j}",
                    source=(i + 1, j),
                    destination=(i, j),
                    lanes=road_num_lanes,
                    speed_limit_mps=road_speed_limit_mps,
                )
            )

    grid = Grid(
        rows=rows,
        cols=cols,
        intersections=intersections,
        roads=roads,
    )

    if output_mode == "verbose":
        print("=== Grid ===")
        print(grid)

    return grid


def generate_random_grid(
    rows: int,
    cols: int,
    road_num_lanes_range: tuple[int],
    road_speed_limit_mps_range: tuple[float],
    seed: int,
    output_mode: str = "verbose",
) -> Grid:
    """
    Generate a random grid using a random seed
    for intersection types
    """
    rng = random.Random(seed)

    intersections = []
    id = 0

    for row in range(rows):
        for col in range(cols):
            intersection_type = rng.choice(
                [member.value for member in IntersectionType]
            )

            intersections.append(
                Intersection(
                    id=id,
                    row=row,
                    col=col,
                    intersection_type=intersection_type,
                )
            )
            id += 1

    roads = []
    num_roads = (rows * (cols - 1) + cols * (rows - 1)) * 2
    road_idx = 0
    road_num_lanes = [
        random.randint(
            road_num_lanes_range[0],
            road_num_lanes_range[1]
        ) for _ in range(num_roads)
    ]
    road_speed_limit_mps = np.linspace(
        road_speed_limit_mps_range[0],
        road_speed_limit_mps_range[1],
        num_roads
    ).tolist()

    # Horizontal edges
    for i in range(rows):
        for j in range(cols - 1):
            roads.append(
                Road(
                    id=f"east_{i}_{j}",
                    source=(i, j),
                    destination=(i, j + 1),
                    lanes=road_num_lanes[road_idx],
                    speed_limit_mps=road_speed_limit_mps[road_idx],
                )
            )
            road_idx += 1
            roads.append(
                Road(
                    id=f"west_{i}_{j + 1}",
                    source=(i, j + 1),
                    destination=(i, j),
                    lanes=road_num_lanes[road_idx],
                    speed_limit_mps=road_speed_limit_mps[road_idx],
                )
            )
            road_idx += 1

    # Vertical edges
    for i in range(rows - 1):
        for j in range(cols):
            roads.append(
                Road(
                    id=f"south_{i}_{j}",
                    source=(i, j),
                    destination=(i + 1, j),
                    lanes=road_num_lanes[road_idx],
                    speed_limit_mps=road_speed_limit_mps[road_idx],
                )
            )
            road_idx += 1
            roads.append(
                Road(
                    id=f"north_{i + 1}_{j}",
                    source=(i + 1, j),
                    destination=(i, j),
                    lanes=road_num_lanes[road_idx],
                    speed_limit_mps=road_speed_limit_mps[road_idx],
                )
            )
            road_idx += 1

    grid = Grid(
        rows=rows,
        cols=cols,
        seed=seed,
        intersections=intersections,
        roads=roads,
        edge_weights=np.ones((rows, cols))
    )

    if output_mode == "verbose":
        print("=== Grid ===")
        print(grid)

    return grid
