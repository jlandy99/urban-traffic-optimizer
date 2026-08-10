from dataclasses import dataclass


@dataclass
class Road:
    id: str
    source: tuple[int]
    destination: tuple[int]
    length_m: float = 1.0 # all roads currently unit length
    lanes: int = 1
    speed_limit_mps: float = 13.89

    def __post_init__(self) -> None:
        if self.length_m <= 0:
            raise ValueError("Road length must be positive.")

        if self.lanes < 1:
            raise ValueError("A road must have at least one lane.")

        if self.speed_limit_mps <= 0:
            raise ValueError("Speed limit must be positive.")

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "destination": self.destination,
            "length_m": self.length_m,
            "lanes": self.lanes,
            "speed_limit_mps": self.speed_limit_mps,
        }
