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
    seed: int | None = None
    edge_weights: list[list[float]] = None

    def __post_init__(self):
        # For now, initialize all edge weights in the Grid to 1
        self.edge_weights = np.ones((self.rows, self.cols))

    def to_dict(self) -> dict:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "seed": self.seed,
            "intersections": [
                intersection.to_dict() for intersection in self.intersections
            ],
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
    output_mode: str = "verbose",
) -> Grid:
    if mode == GridMode.ALL_PRIORITY:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.PRIORITY,
            output_mode=output_mode,
        )
    elif mode == GridMode.ALL_PRIORITY_STOP:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.PRIORITY_STOP,
            output_mode=output_mode,
        )
    elif mode == GridMode.ALL_ALLWAY_STOP:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.ALLWAY_STOP,
            output_mode=output_mode,
        )
    elif mode == GridMode.ALL_TRAFFIC_LIGHT:
        return generate_uniform_grid(
            rows=rows,
            cols=cols,
            intersection_type=IntersectionType.TRAFFIC_LIGHT,
            output_mode=output_mode,
        )
    elif mode == GridMode.RANDOM:
        return generate_random_grid(
            rows=rows,
            cols=cols,
            seed=seed,
            output_mode=output_mode,
        )


def generate_uniform_grid(
    rows: int,
    cols: int,
    intersection_type: IntersectionType,
    output_mode: str = "verbose",
) -> Grid:
    """
    Generate a uniform grid using a specified intersection type
    """

    intersections = []
    id = 0

    for row in range(rows):
        for col in range(cols):
            intersections.append(
                Intersection(
                    id=id,
                    row=row,
                    col=col,
                    intersection_type=intersection_type,
                )
            )
            id += 1

    grid = Grid(
        rows=rows,
        cols=cols,
        intersections=intersections,
    )

    if output_mode == "verbose":
        print("=== Grid ===")
        print(grid)

    return grid


def generate_random_grid(
    rows: int,
    cols: int,
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

    grid = Grid(
        rows=rows,
        cols=cols,
        seed=seed,
        intersections=intersections,
    )

    if output_mode == "verbose":
        print("=== Grid ===")
        print(grid)

    return grid
