from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np
from spisea import atmospheres
from spisea import evolution
from spisea import reddening
from spisea import synthetic as syn

PROJECT_DIR = Path("/workspace")
ISO_DIR = PROJECT_DIR / "isochrones"
ISO_DIR.mkdir(parents=True, exist_ok=True)

LOG_AGE_RANGE = np.arange(9.0, 10.11, 0.25)
AKS_RANGE = np.arange(0.2, 1.0, 0.2)
DISTANCE_RANGE = np.arange(7000, 9000, 500)
METALLICITY_RANGE = [-0.5, 0.0, 0.2]

FILTERS = [
    "roman,wfi,f062",
    "roman,wfi,f087",
    "roman,wfi,f106",
    "roman,wfi,f129",
    "roman,wfi,f146",
    "roman,wfi,f158",
    "roman,wfi,f184",
    "roman,wfi,f213",
]

EVO_MODEL = evolution.MISTv1()
ATM_FUNC = atmospheres.get_merged_atmosphere
RED_LAW = reddening.RedLawFritz11(scale_lambda=2.166)


def destination_path(
    log_age: float,
    aks: float,
    distance: int,
    metallicity: float,
) -> Path:
    return ISO_DIR / (
        f"iso_logAge{log_age:.2f}"
        f"_AKs{aks:.2f}"
        f"_dist{distance}"
        f"_metal{metallicity:+.2f}.fits"
    )


def generate_one(
    log_age: float,
    aks: float,
    distance: int,
    metallicity: float,
) -> bool:
    destination = destination_path(log_age, aks, distance, metallicity)

    if destination.exists():
        print(f"SKIP {destination.name}")
        return True

    print(
        "GENERATE",
        f"logAge={log_age:.2f}",
        f"AKs={aks:.2f}",
        f"distance={distance}",
        f"metallicity={metallicity:+.2f}",
    )

    try:
        iso = syn.IsochronePhot(
            logAge=float(log_age),
            AKs=float(aks),
            distance=float(distance),
            metallicity=float(metallicity),
            iso_dir=str(ISO_DIR),
            evo_model=EVO_MODEL,
            atm_func=ATM_FUNC,
            red_law=RED_LAW,
            filters=FILTERS,
            mag_sys="AB",
        )

        table = iso.points
        table.meta["LOGAGE"] = float(log_age)
        table.meta["AKS"] = float(aks)
        table.meta["DISTANCE"] = float(distance)
        table.meta["METALLICITY"] = float(metallicity)
        table.write(destination, format="fits", overwrite=True)

        print(f"SAVED {destination}")
        return True
    except Exception as exc:
        print(f"FAILED {destination.name}: {exc}")
        return False


def main() -> None:
    attempted = 0
    succeeded = 0

    for values in itertools.product(
        LOG_AGE_RANGE,
        AKS_RANGE,
        DISTANCE_RANGE,
        METALLICITY_RANGE,
    ):
        attempted += 1
        succeeded += int(
            generate_one(
                float(values[0]),
                float(values[1]),
                int(values[2]),
                float(values[3]),
            )
        )

    print(f"Attempted: {attempted}")
    print(f"Successful or cached: {succeeded}")
    print(f"Failed: {attempted - succeeded}")


if __name__ == "__main__":
    main()
