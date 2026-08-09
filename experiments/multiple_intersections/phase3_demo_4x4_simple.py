from traffic_optimizer.network.grid import generate_random_grid


def main() -> None:
    grid = generate_random_grid(
        rows=4,
        cols=4,
        seed=42,
    )

    print("4x4 Intersection Grid")
    print(f"Seed: {grid.seed}")
    print()
    print(grid)
    print()
    print(grid.to_json())


if __name__ == "__main__":
    main()
