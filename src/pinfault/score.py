# Copyright 2026 Digital Currensy Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math


def _bad(value: float | None) -> bool:
    return value is not None and not math.isfinite(value)


def integrity(void_fraction: float | None, slope_deg: float | None, offset_m: float | None) -> str:
    if _bad(void_fraction) or _bad(slope_deg) or _bad(offset_m):
        return "missing"
    if void_fraction is None or void_fraction < 0 or void_fraction > 1:
        return "missing"
    if void_fraction > 0.15:
        return "voids"
    if slope_deg is None:
        return "missing"
    if slope_deg < 0:
        return "missing"
    if slope_deg > 20:
        return "slope"
    if offset_m is None:
        return "missing"
    if offset_m < 0:
        return "missing"
    if offset_m > 30:
        return "offset"
    return "ok"


def grade_deg(rise_m: float, run_m: float) -> float | None:
    """Degrees from a rise and a horizontal run. The run has to be positive."""
    if not math.isfinite(rise_m) or not math.isfinite(run_m) or run_m <= 0:
        return None
    return math.degrees(math.atan(rise_m / run_m))
