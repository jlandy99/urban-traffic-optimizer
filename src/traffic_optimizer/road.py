from dataclasses import dataclass


@dataclass
class Road:
    id: str
    source: str
    destination: str
    length_m: float
    lanes: int = 1
    speed_limit_kmh: float = 50.0

    def __post_init__(self) -> None:
        if self.length_m <= 0:
            raise ValueError("Road length must be positive.")

        if self.lanes < 1:
            raise ValueError("A road must have at least one lane.")

        if self.speed_limit_kmh <= 0:
            raise ValueError("Speed limit must be positive.")
