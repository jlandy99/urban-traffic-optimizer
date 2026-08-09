from pathlib import Path

from traffic_optimizer.network.demand import generate_traffic_demand
from traffic_optimizer.network.grid import generate_random_grid
from traffic_optimizer.network.sumo_network import generate_sumo_network
from traffic_optimizer.simulation.results import save_results
from traffic_optimizer.simulation.simulation import run_simulation


def main() -> None:
    output_dir = Path("outputs/simulations/grid_4x4_seed_42")

    grid = generate_random_grid(
        rows=4,
        cols=4,
        seed=42,
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
        num_vehicles=10,
        seed=42,
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
