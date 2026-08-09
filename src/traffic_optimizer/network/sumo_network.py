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

    for intersection in grid.intersections:
        row = intersection.row
        col = intersection.col

        # Horizontal connection (east / west)
        if col > 0:
            edge_lines.append(
                f'    <edge id="west_{row}_{col}" '
                f'from="node_{row}_{col}" '
                f'to="node_{row}_{col - 1}" '
                f'numLanes="1" speed="13.89"/>'
            )
        if col < grid.cols - 1:
            edge_lines.append(
                f'    <edge id="east_{row}_{col}" '
                f'from="node_{row}_{col}" '
                f'to="node_{row}_{col + 1}" '
                f'numLanes="1" speed="13.89"/>'
            )

        # Vertical connection (north / south)
        if row > 0:
            edge_lines.append(
                f'    <edge id="north_{row}_{col}" '
                f'from="node_{row}_{col}" '
                f'to="node_{row - 1}_{col}" '
                f'numLanes="1" speed="13.89"/>'
            )
        if row < grid.rows - 1:
            edge_lines.append(
                f'    <edge id="south_{row}_{col}" '
                f'from="node_{row}_{col}" '
                f'to="node_{row + 1}_{col}" '
                f'numLanes="1" speed="13.89"/>'
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
