import random
from pathlib import Path

from traffic_optimizer.network.grid import Grid
from traffic_optimizer.network.topology import Topology


def generate_traffic_demand(
    grid: Grid,
    output_dir: Path,
    num_vehicles: int = 100,
    seed: int = 42,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    routes_file = output_dir / "routes.rou.xml"

    rng = random.Random(seed)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<routes>",
        '    <vType id="car" accel="2.6" decel="4.5" '
        'sigma="0.5" length="5" maxSpeed="13.89"/>',
    ]

    for vehicle_id in range(num_vehicles):
        # We want to start from vertices
        origin = (
            rng.randrange(grid.rows),
            rng.randrange(grid.cols),
        )
        destination = (
            rng.randrange(grid.rows),
            rng.randrange(grid.cols),
        )
        # Fail safe: make sure the origin isn't the same as destination
        while destination == origin:
            destination = (
                rng.randrange(grid.rows),
                rng.randrange(grid.cols),
            )

        # Choose the shortest (valid) path between the origin and destination
        topology = Topology()
        path = topology.shortest_path(
            origin,
            destination,
            grid.rows,
            grid.cols,
            grid.edge_weights,
        )

        # Convert into edges consumable by SUMO
        route_edges = topology.path_to_sumo_edges(path)
        route_str = " ".join(route_edges)

        lines.append(
            f'    <vehicle id="veh_{vehicle_id}" ' f'type="car" depart="{vehicle_id}">'
        )
        lines.append(f'        <route edges="{route_str}"/>')
        lines.append("    </vehicle>")

    lines.append("</routes>")

    routes_file.write_text("\n".join(lines))

    return routes_file
