from traffic_optimizer.intersection import Approach, ControlType, Intersection


intersection = Intersection(
    id="I_0",
    control_type=ControlType.SIGNAL,
    north=Approach(
        lanes=2,
        left_turn_lane=True,
        bike_lane=True,
    ),
    south=Approach(
        lanes=2,
        left_turn_lane=True,
        bike_lane=True,
    ),
    east=Approach(
        lanes=2,
        bike_lane=True,
    ),
    west=Approach(
        lanes=2,
        bike_lane=True,
    ),
    pedestrian_crossings=True,
)


print(intersection)
