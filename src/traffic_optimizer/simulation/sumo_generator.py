import subprocess
from pathlib import Path


def generate_single_intersection(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    nodes_file = output_dir / "nodes.nod.xml"
    edges_file = output_dir / "edges.edg.xml"
    network_file = output_dir / "network.net.xml"

    nodes_file.write_text(
        """\
<nodes>
    <node id="center" x="0" y="0" type="traffic_light"/>
    <node id="north" x="0" y="500"/>
    <node id="south" x="0" y="-500"/>
    <node id="east" x="500" y="0"/>
    <node id="west" x="-500" y="0"/>
</nodes>
"""
    )

    edges_file.write_text(
        """\
<edges>
    <edge id="north_to_center" from="north" to="center"
          numLanes="2" speed="13.89"/>
    <edge id="center_to_north" from="center" to="north"
          numLanes="2" speed="13.89"/>

    <edge id="south_to_center" from="south" to="center"
          numLanes="2" speed="13.89"/>
    <edge id="center_to_south" from="center" to="south"
          numLanes="2" speed="13.89"/>

    <edge id="east_to_center" from="east" to="center"
          numLanes="2" speed="13.89"/>
    <edge id="center_to_east" from="center" to="east"
          numLanes="2" speed="13.89"/>

    <edge id="west_to_center" from="west" to="center"
          numLanes="2" speed="13.89"/>
    <edge id="center_to_west" from="center" to="west"
          numLanes="2" speed="13.89"/>
</edges>
"""
    )

    subprocess.run(
        [
            "netconvert",
            "--node-files",
            str(nodes_file),
            "--edge-files",
            str(edges_file),
            "--output-file",
            str(network_file),
        ],
        check=True,
    )

    return network_file
