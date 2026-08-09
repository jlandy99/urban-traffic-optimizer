import argparse
import sys
from pathlib import Path

from traffic_optimizer.network.demand import generate_traffic_demand
from traffic_optimizer.network.grid import generate_grid
from traffic_optimizer.network.sumo_network import generate_sumo_network
from traffic_optimizer.simulation.results import save_results
from traffic_optimizer.simulation.simulation import run_simulation


def main(args: list[str] | None = None) -> int:
    # Parse command line flags
    parser = argparse.ArgumentParser(
        description="A script to process graph paths or file structures."
    )
    parser.add_argument(
        "--num-vehicles",
        type=int,
        default=20,
        help="Number of vehicles to run through the simulation (default: 20)."
    )
    parser.add_argument(
        "--grid-type",
        type=int,
        default=1,
        help="Type of grid. Options: [1] random, [2] all stop, [3] all signal, [4] all roundabout (default: 1)."
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
        help="Random seed for grid initialization (default: 42). Only used if --grid-type=1 (random)."
    )
    parser.add_argument(
        "--random-seed-traffic",
        type=int,
        default=42,
        help="Random seed for traffic initialization (default: 42)."
    )

    # Set variables
    args = parser.parse_args()
    num_vehicles = args.num_vehicles
    grid_type = args.grid_type
    rows = args.num_rows
    cols = args.num_cols
    random_seed_grid = args.random_seed_grid
    random_seed_traffic = args.random_seed_traffic

    # Start simulation
    output_dir = Path("outputs/simulations/grid_4x4_seed_42")

    grid = generate_grid(
        rows=rows,
        cols=cols,
        seed=random_seed_grid,
        mode=grid_type,
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
