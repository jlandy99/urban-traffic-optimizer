import json
import numpy as np
import xml.etree.ElementTree as ET
from pathlib import Path

import traci


def gini(values):
    values = np.asarray(values, dtype=float)

    if len(values) == 0:
        return 0.0

    if np.any(values < 0):
        raise ValueError("Gini requires non-negative values.")

    if np.all(values == 0):
        return 0.0

    sorted_values = np.sort(values)
    n = len(sorted_values)

    return (
        (2 * np.sum((np.arange(1, n + 1)) * sorted_values))
        / (n * np.sum(sorted_values))
        - (n + 1) / n
    )


def run_simulation(
    network_file: Path,
    routes_file: Path,
    output_dir: Path,
    end_time: int = 300,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    config_file = output_dir / "simulation.sumocfg"
    tripinfo_file = (output_dir / "tripinfo.xml").resolve()

    config_file.write_text(
        f"""\
            <configuration>
                <input>
                    <net-file value="{network_file.name}"/>
                    <route-files value="{routes_file.name}"/>
                </input>

                <output>
                    <tripinfo-output value="{tripinfo_file}"/>
                </output>

                <time>
                    <begin value="0"/>
                    <end value="{end_time}"/>
                </time>
            </configuration>
        """
    )

    log_file = output_dir / "sumo.log"

    traci.start(
        [
            "sumo",
            "-c",
            str(config_file),
            "--no-step-log",
            "--no-warnings",
            "--log",
            str(log_file),
        ]
    )

    departed = set()
    arrived = set()

    total_waiting_time = 0.0
    total_speed = 0.0
    speed_samples = 0
    num_vehicles = 0

    step = 0
    max_steps = 10_000

    vehicle_metrics = {}

    while traci.simulation.getMinExpectedNumber() > 0 and step < max_steps:
        traci.simulationStep()
        step += 1

        vehicle_ids = traci.vehicle.getIDList()
        num_vehicles = len(vehicle_ids)

        departed_ids = traci.simulation.getDepartedIDList()
        arrived_ids = traci.simulation.getArrivedIDList()

        departed.update(departed_ids)
        arrived.update(arrived_ids)

        # Capture live state for vehicles currently in SUMO
        for vehicle_id in traci.vehicle.getIDList():
            total_speed += traci.vehicle.getSpeed(vehicle_id)
            speed_samples += 1

    traci.close()

    tree = ET.parse(tripinfo_file)
    root = tree.getroot()

    # Grab per-vehicle metrics
    per_vehicle_metrics = {}
    for tripinfo in root.findall("tripinfo"):
        vehicle_id = tripinfo.attrib["id"]

        per_vehicle_metrics[vehicle_id] = {
            "depart_time_s": float(tripinfo.attrib["depart"]),
            "arrival_time_s": float(tripinfo.attrib["arrival"]),
            "travel_time_s": float(tripinfo.attrib["duration"]),
            "route_length_m": float(tripinfo.attrib["routeLength"]),
            "waiting_time_s": float(tripinfo.attrib["waitingTime"]),
            "time_loss_s": float(tripinfo.attrib["timeLoss"]),
        }

    # Calculate cumulative metrics
    total_waiting_time = sum(
        vehicle["waiting_time_s"]
        for vehicle in per_vehicle_metrics.values()
    )
    total_travel_time = sum(
        vehicle["travel_time_s"]
        for vehicle in per_vehicle_metrics.values()
    )
    average_travel_time = (
        total_travel_time / len(per_vehicle_metrics)
        if per_vehicle_metrics
        else 0.0
    )
    average_speed = total_speed / speed_samples if speed_samples > 0 else 0.0

    # Calculate distribution of waiting times
    waiting_times = [
        vehicle["waiting_time_s"]
        for vehicle in per_vehicle_metrics.values()
    ]
    # Interpretation of Gini:
    # 0.00 → perfectly equal waiting times
    # 0.10 → very uniform
    # 0.30 → noticeable inequality
    # 0.50+ → substantial inequality
    # 1.00 → extreme inequality
    waiting_gini = gini(waiting_times)

    distribution_travel_time_metrics = {
        "waiting_mean_s": round(np.mean(waiting_times), 3),
        "waiting_median_s": round(np.median(waiting_times), 3),
        "waiting_std_s": round(np.std(waiting_times), 3),
        "waiting_p95_s": round(np.percentile(waiting_times, 95), 3),
        "waiting_max_s": round(np.max(waiting_times), 3),
        "waiting_gini": waiting_gini,
    }

    # Calculate route length distributions
    route_lengths = [
        vehicle["route_length_m"]
        for vehicle in per_vehicle_metrics.values()
    ]
    distribution_route_length_metrics = {
        "length_mean_m": round(np.mean(route_lengths), 3),
        "length_median_m": round(np.median(route_lengths), 3),
        "length_std_m": round(np.std(route_lengths), 3),
        "length_max_m": round(np.max(route_lengths), 3),
    }

    # Print Output
    print("\n=== Vehicle Summary ===")
    print(f"Expected vehicles:\t{num_vehicles}")
    print(f"Departed:\t\t{len(departed)}")
    print(f"Arrived:\t\t{len(arrived)}")
    print(f"Still active:\t\t{len(departed - arrived)}")

    print("\n=== Travel Times ===")
    print(f"Total waiting time:\t{round(total_waiting_time, 3)}")
    print(f"Total travel time:\t{round(total_travel_time, 3)}")
    print(f"Average travel time:\t{round(average_travel_time, 3)}")
    print(f"Average speed:\t\t{round(average_speed, 3)}")

    print(f"\nWaiting mean:\t\t{distribution_travel_time_metrics['waiting_mean_s']}")
    print(f"Waiting median:\t\t{distribution_travel_time_metrics['waiting_median_s']}")
    print(f"Waiting std:\t\t{distribution_travel_time_metrics['waiting_std_s']}")
    print(f"Waiting p95:\t\t{distribution_travel_time_metrics['waiting_p95_s']}")
    print(f"Waiting max:\t\t{distribution_travel_time_metrics['waiting_max_s']}")
    print(f"Waiting Gini:\t\t{distribution_travel_time_metrics['waiting_gini']}")

    print(f"\nRoute Length mean:\t{distribution_route_length_metrics['length_mean_m']}")
    print(f"Route Length median:\t{distribution_route_length_metrics['length_median_m']}")
    print(f"Route Length std:\t{distribution_route_length_metrics['length_std_m']}")
    print(f"Route Length max:\t{distribution_route_length_metrics['length_max_m']}")

    keys = list(per_vehicle_metrics.keys())
    keys.sort(key=lambda x: int(x.split("_")[1]))
    print("\n=== Per-Vehicle Stats ===")
    for vehicle_id in keys:
        print(vehicle_id)
        print(f"\tTravel time: {per_vehicle_metrics[vehicle_id]['travel_time_s']}")
        print(f"\tWaiting time: {per_vehicle_metrics[vehicle_id]['waiting_time_s']}")
        print(f"\tRoute length: {per_vehicle_metrics[vehicle_id]['route_length_m']}")


    if departed - arrived:
        print(f"Still active IDs:  {sorted(departed - arrived)}")

    return {
        "total_waiting_time_s": round(total_waiting_time, 3),
        "departed_vehicles": len(departed),
        "arrived_vehicles": len(arrived),
        "active_vehicles": len(departed - arrived),
        "average_speed_mps": round(average_speed, 3),
    }
