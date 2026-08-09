import traci


def print_sumo_diagnostics() -> None:
    """Print the traffic-control state SUMO loaded for the current simulation."""

    print("\n=== SUMO DIAGNOSTICS ===")

    # ---------------------------------------------------------
    # Traffic lights
    # ---------------------------------------------------------

    traffic_lights = traci.trafficlight.getIDList()

    print(f"Traffic lights: {len(traffic_lights)}")

    if traffic_lights:
        for tls_id in traffic_lights:
            print(
                f"  TLS {tls_id}: "
                f"phase={traci.trafficlight.getPhase(tls_id)}, "
                f"duration={traci.trafficlight.getPhaseDuration(tls_id)}, "
                f"state={traci.trafficlight.getRedYellowGreenState(tls_id)}"
            )

    # ---------------------------------------------------------
    # Junctions
    # ---------------------------------------------------------

    junction_ids = traci.junction.getIDList()

    print(f"Junctions: {len(junction_ids)}")

    for junction_id in junction_ids[:10]:
        try:
            position = traci.junction.getPosition(junction_id)
            print(f"  Junction {junction_id}: position={position}")
        except Exception:
            pass

    # ---------------------------------------------------------
    # Vehicles
    # ---------------------------------------------------------

    vehicle_ids = traci.vehicle.getIDList()

    print(f"Active vehicles: {len(vehicle_ids)}")

    if vehicle_ids:
        for vehicle_id in vehicle_ids[:10]:
            print(
                f"  Vehicle {vehicle_id}: "
                f"road={traci.vehicle.getRoadID(vehicle_id)}, "
                f"speed={traci.vehicle.getSpeed(vehicle_id):.2f}, "
                f"waiting={traci.vehicle.getWaitingTime(vehicle_id):.2f}"
            )

    print("========================\n")
