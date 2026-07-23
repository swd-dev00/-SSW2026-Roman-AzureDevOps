from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

workspace = Path("/workspace")

print("Python:", sys.version)
print("Workspace:", workspace)
print("PYSYN_CDBS:", os.environ.get("PYSYN_CDBS"))
print("SPISEA_MODELS:", os.environ.get("SPISEA_MODELS"))

usage = shutil.disk_usage(workspace)
print(f"Free workspace space: {usage.free / 1024**3:.2f} GB")

from spisea import synthetic as syn

print("SPISEA import successful.")

roman_filter_candidates = [
    "roman,wfi,f146",
    "roman,wfi,F146",
]

last_error = None
for filter_name in roman_filter_candidates:
    try:
        info = syn.get_filter_info(filter_name)
        print(f"Roman filter loaded: {filter_name}")
        print(info)
        break
    except Exception as exc:
        last_error = exc
else:
    raise RuntimeError(
        "Roman F146 throughput could not be loaded. "
        "Verify the container's CDBS data and the filter identifier used by "
        "the official workshop notebook."
    ) from last_error
