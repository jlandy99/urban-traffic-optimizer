import argparse
import sys
from pathlib import Path

from traffic_optimizer.network.demand import generate_traffic_demand
from traffic_optimizer.network.grid import generate_random_grid
from traffic_optimizer.network.sumo_network import generate_sumo_network
from traffic_optimizer.simulation.results import save_results
from traffic_optimizer.simulation.simulation import run_simulation


def main(args: list[str] | None = None) -> int:
    # Parse command line flags
    parser = argparse.ArgumentParser(
        description="A script to process graph paths or file structures."
    )
    parser.add_argument(
        "num-vehicles",
        type=int,
        help="Number of vehicles to run through the simulation."
    )
    parser.add_argument(
        "--num-rows",
        type=int,
        default=4,
        help="Number of rows in grid network (default: 4)."
    )
    parser.add_argument(
        "--num-cols",
        type=int,
        default=4,
        help="Number of rows in grid network (default: 4)."
    )
    parser.add_argument(
        "--random-seed-grid",
        type=int,
        default=42,
        help="Random seed for grid initialization (default: 42)."
    )
    parser.add_argument(
        "--random-seed-traffic",
        type=int,
        default=42,
        help="Random seed for traffic initialization (default: 42)."
    )
    parsed_args = parser.parse_args(args)

    # Set variables
    num_vehicles = parser.num_vehicles
    rows = parser.num_rows
    cols = parser.num_cols
    random_seed_grid = parser.random_seed_grid
    random_seed_traffic = parser.random_seed_traffic

    # Start simulation
    output_dir = Path("outputs/simulations/grid_4x4_seed_42")

    grid = generate_random_grid(
        rows=rows,
        cols=cols,
        seed=random_seed_grid,
    )

    print("Generated grid:")
    print(grid)
    print()

    network_file = generate_sumo_network(
        grid=grid,
        output_dir=output_dir,
    )

    routes_file = generate_traffic_demand(
        grid=grid,
        output_dir=output_dir,
        num_vehicles=num_vehicles,
        seed=random_seed_traffic,
    )

    metrics = run_simulation(
        network_file=network_file,
        routes_file=routes_file,
        output_dir=output_dir,
    )

    results_file = save_results(
        grid=grid,
        metrics=metrics,
        output_dir=output_dir,
    )

    print("Simulation complete.")


if __name__ == "__main__":
    main()
