from pathlib import Path

from traffic_optimizer.sumo_generator import generate_single_intersection


output_dir = Path("outputs/simulations/phase2_demo")

network_file = generate_single_intersection(output_dir)

print(f"Generated SUMO network: {network_file}")
