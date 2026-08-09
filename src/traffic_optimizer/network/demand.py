import random
from pathlib import Path

from traffic_optimizer.network.grid import Grid


def generate_traffic_demand(
    grid: Grid,
    output_dir: Path,
    num_vehicles: int = 100,
    seed: int = 42,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    routes_file = output_dir / "routes.rou.xml"

    rng = random.Random(seed)

    possible_edges = []

    # Horizontal edges
    for row in range(grid.rows):
        for col in range(grid.cols - 1):
            possible_edges.append(f"east_{row}_{col}")
            possible_edges.append(f"west_{row}_{col}")

    # Vertical edges
    for row in range(grid.rows - 1):
        for col in range(grid.cols):
            possible_edges.append(f"south_{row}_{col}")
            possible_edges.append(f"north_{row}_{col}")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<routes>",
        '    <vType id="car" accel="2.6" decel="4.5" '
        'sigma="0.5" length="5" maxSpeed="13.89"/>',
    ]

    for vehicle_id in range(num_vehicles):
        origin, destination = rng.sample(possible_edges, 2)

        lines.append(
            f'    <vehicle id="veh_{vehicle_id}" ' f'type="car" depart="{vehicle_id}">'
        )

        # This is intentionally temporary.
        # We'll replace it with actual route calculation.
        lines.append(f'        <route edges="{origin} {destination}"/>')

        lines.append("    </vehicle>")

    lines.append("</routes>")

    routes_file.write_text("\n".join(lines))

    return routes_file
