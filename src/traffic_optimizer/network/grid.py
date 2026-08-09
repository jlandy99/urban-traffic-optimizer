import json
import random
from dataclasses import dataclass, field

from .intersection import Intersection, IntersectionType
from .road import Road


@dataclass
class Grid:
    rows: int
    cols: int
    seed: int
    intersections: list[Intersection]

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


def generate_random_grid(
    rows: int,
    cols: int,
    seed: int,
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

    return Grid(
        rows=rows,
        cols=cols,
        seed=seed,
        intersections=intersections,
    )

    grid = Grid()
    return grid
