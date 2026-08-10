import subprocess
from pathlib import Path

from traffic_optimizer.network.grid import Grid
from traffic_optimizer.network.intersection import SUMO_NODE_TYPES


def generate_sumo_network(
    grid: Grid,
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    nodes_file = output_dir / "nodes.nod.xml"
    edges_file = output_dir / "edges.edg.xml"
    network_file = output_dir / "network.net.xml"

    # ---------------------------------------------------------
    # 1. Create SUMO nodes
    # ---------------------------------------------------------

    node_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<nodes>",
    ]

    spacing = 100.0

    for intersection in grid.intersections:
        x = intersection.col * spacing
        y = intersection.row * spacing

        node_lines.append(
            f'    <node id="node_{intersection.row}_{intersection.col}" '
            f'x="{x}" y="{y}" type="{SUMO_NODE_TYPES[intersection.intersection_type]}"/>'
        )

    node_lines.append("</nodes>")

    nodes_file.write_text("\n".join(node_lines))

    # ---------------------------------------------------------
    # 2. Create SUMO edges
    # ---------------------------------------------------------

    edge_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<edges>",
    ]

    for road in grid.roads:
        edge_lines.append(
            f'    <edge id="{road.id}" '
            f'from="node_{road.source[0]}_{road.source[1]}" '
            f'to="node_{road.destination[0]}_{road.destination[1]}" '
            f'numLanes="{road.lanes}" speed="{road.speed_limit_mps}"/>'
        )

    edge_lines.append("</edges>")

    edges_file.write_text("\n".join(edge_lines))

    # ---------------------------------------------------------
    # 3. Convert to SUMO network
    # ---------------------------------------------------------

    subprocess.run(
        [
            "netconvert",
            "--node-files",
            str(nodes_file),
            "--edge-files",
            str(edges_file),
            "--output-file",
            str(network_file),
            "--tls.guess",
        ],
        check=True,
    )

    return network_file
