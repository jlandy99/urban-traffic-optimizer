import json
from pathlib import Path


def save_results(
    grid,
    metrics: dict,
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "grid": grid.to_dict(),
        "metrics": metrics,
    }

    results_file = output_dir / "results.json"

    results_file.write_text(
        json.dumps(
            results,
            indent=2,
        )
    )

    return results_file
