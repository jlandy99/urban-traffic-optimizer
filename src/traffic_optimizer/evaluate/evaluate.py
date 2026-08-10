import sys
from pathlib import Path
from dataclasses import dataclass
from traffic_optimizer.network.grid import GridMode
from traffic_optimizer.network.topology import RoutingAlgorithm
from traffic_optimizer.network.sumo_network import generate_sumo_network
from traffic_optimizer.network.grid import generate_grid
from traffic_optimizer.network.demand import generate_traffic_demand
from traffic_optimizer.simulation.simulation import run_simulation
from traffic_optimizer.simulation.results import save_results

@dataclass
class ScenarioConfig:
    rows: int
    cols: int
    grid_type: GridMode
    num_vehicles: int
    random_seed_grid: int
    random_seed_traffic: int
    routing_algorithm: RoutingAlgorithm = RoutingAlgorithm.DJIKSTRAS
    road_num_lanes: int = 1,
    road_speed_limit_mps: float = 13.89,
    road_num_lanes_range: tuple[int] = (1, 3),
    road_speed_limit_mps_range: tuple[float] = (10.0, 25.0),
    filename: str = "temp"
    verbose: bool = False


@dataclass
class Metrics:
    efficiency: float
    uniformity: float
    cost: float


def evaluate_scenario(
    config: ScenarioConfig,
):
    grid = generate_grid(
        rows=config.rows,
        cols=config.cols,
        seed=config.random_seed_grid,
        mode=config.grid_type,
        road_num_lanes=config.road_num_lanes,
        road_speed_limit_mps=config.road_speed_limit_mps,
        road_num_lanes_range=config.road_num_lanes_range,
        road_speed_limit_mps_range=config.road_speed_limit_mps_range,
    )
    output_dir = Path(f"outputs/simulations/{config.filename}")
    network_file = generate_sumo_network(
        grid=grid,
        output_dir=output_dir,
    )
    routes_file = generate_traffic_demand(
        grid=grid,
        output_dir=output_dir,
        num_vehicles=config.num_vehicles,
        seed=config.random_seed_traffic,
    )
    metrics = run_simulation(
        network_file=network_file,
        routes_file=routes_file,
        output_dir=output_dir,
        diagnostic_mode=config.verbose,
    )
    results_file = save_results(
        grid=grid,
        metrics=metrics,
        output_dir=output_dir,
    )
    return metrics
