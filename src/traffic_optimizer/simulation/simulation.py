import json
from pathlib import Path

import traci


def run_simulation(
    network_file: Path,
    routes_file: Path,
    output_dir: Path,
    end_time: int = 300,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    config_file = output_dir / "simulation.sumocfg"

    config_file.write_text(
        f"""\
<configuration>
    <input>
        <net-file value="{network_file.name}"/>
        <route-files value="{routes_file.name}"/>
    </input>

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

    total_waiting_time = 0.0
    total_speed = 0.0
    speed_samples = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        vehicle_ids = traci.vehicle.getIDList()

        for vehicle_id in vehicle_ids:
            total_waiting_time += traci.vehicle.getWaitingTime(vehicle_id)

            total_speed += traci.vehicle.getSpeed(vehicle_id)

            speed_samples += 1

    completed_vehicles = traci.simulation.getArrivedNumber()

    traci.close()

    average_speed = total_speed / speed_samples if speed_samples > 0 else 0.0

    return {
        "total_waiting_time_s": round(total_waiting_time, 3),
        "completed_vehicles": completed_vehicles,
        "average_speed_mps": round(average_speed, 3),
    }
