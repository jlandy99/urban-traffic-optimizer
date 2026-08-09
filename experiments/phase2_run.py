import json
import subprocess
from pathlib import Path

import traci


OUTPUT_DIR = Path("outputs/simulations/phase2_demo")


def create_routes() -> Path:
    routes_file = OUTPUT_DIR / "routes.rou.xml"

    routes_file.write_text(
        """\
<routes>

    <vType
        id="car"
        accel="2.6"
        decel="4.5"
        sigma="0.5"
        length="5"
        maxSpeed="13.89"
    />

    <route id="west_east"
           edges="west_to_center center_to_east"/>

    <route id="east_west"
           edges="east_to_center center_to_west"/>

    <route id="north_south"
           edges="north_to_center center_to_south"/>

    <route id="south_north"
           edges="south_to_center center_to_north"/>

    <vehicle
        id="veh_west_east"
        type="car"
        route="west_east"
        depart="0"
    />

    <vehicle
        id="veh_east_west"
        type="car"
        route="east_west"
        depart="5"
    />

    <vehicle
        id="veh_north_south"
        type="car"
        route="north_south"
        depart="10"
    />

    <vehicle
        id="veh_south_north"
        type="car"
        route="south_north"
        depart="15"
    />

</routes>
"""
    )

    return routes_file


def create_config(routes_file: Path) -> Path:
    config_file = OUTPUT_DIR / "simulation.sumocfg"

    config_file.write_text(
        f"""\
<configuration>
    <input>
        <net-file value="network.net.xml"/>
        <route-files value="{routes_file.name}"/>
    </input>

    <time>
        <begin value="0"/>
        <end value="120"/>
    </time>
</configuration>
"""
    )

    return config_file


def run_simulation(config_file: Path) -> dict:
    traci.start(
        [
            "sumo",
            "-c",
            str(config_file),
            "--no-step-log",
            "--no-warnings",
            "--log",
            str(OUTPUT_DIR / "sumo.log"),
        ]
    )

    total_waiting_time = 0.0
    total_travel_time = 0.0
    completed_vehicles = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        for vehicle_id in traci.vehicle.getIDList():
            total_waiting_time += traci.vehicle.getWaitingTime(vehicle_id)

    completed_vehicles = traci.simulation.getArrivedNumber()

    traci.close()

    return {
        "total_waiting_time_s": round(total_waiting_time, 3),
        "completed_vehicles": completed_vehicles,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    routes_file = create_routes()
    config_file = create_config(routes_file)

    print(f"Routes: {routes_file}")
    print(f"Config: {config_file}")

    metrics = run_simulation(config_file)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
