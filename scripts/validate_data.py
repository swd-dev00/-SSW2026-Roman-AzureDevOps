from pathlib import Path

required = [
    Path("/workspace/data/events_table.parquet"),
    Path("/workspace/data/stars_table.parquet"),
    Path("/workspace/data/sim_pops_table.parquet"),
]

missing = [str(path) for path in required if not path.exists()]
if missing:
    raise FileNotFoundError(
        "Missing workshop data files:\n- " + "\n- ".join(missing)
    )

for path in required:
    print(f"FOUND {path} ({path.stat().st_size / 1024**2:.2f} MB)")
