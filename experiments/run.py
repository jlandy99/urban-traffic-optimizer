import argparse
from traffic_optimizer.evaluate.evaluate import ScenarioConfig, evaluate_scenario

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
        help="Type of grid. Options: [1] random, [2] all priority (minor yields to major), [3] all priority stop (2-way), [4] all allway stop, [5] all traffic light, [6] all roundabout -- to be implemented (default: 1)."
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
    parser.add_argument(
        "--routing-algorithm",
        type=str,
        default="djikstras",
        help="Routing algorithm to use for vehicles between origin and destination. Options include ['bfs', 'djikstras'] (default: 'djikstras')."
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="temp",
        help="Filename to save the experimental data on; if empty ('temp'), no folder will be written (default: 'temp')."
    )
    parser.add_argument(
        "--verbose",
        action=argparse.BooleanOptionalAction,
        help="Verbose mode; when set, leverage diagnostic mode."
    )

    # Set variables
    args = parser.parse_args()
    scenario = ScenarioConfig(
        rows=args.num_rows,
        cols=args.num_cols,
        grid_type=args.grid_type,
        num_vehicles=args.num_vehicles,
        random_seed_grid=args.random_seed_grid,
        random_seed_traffic=args.random_seed_traffic,
        routing_algorithm=args.routing_algorithm,
        filename=args.filename,
    )
    metrics = evaluate_scenario(scenario)
    print("\n=== Simulation Results ===")
    print(metrics)


if __name__ == "__main__":
    main()
