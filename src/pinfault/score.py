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

def integrity(void_fraction: float | None, slope_deg: float | None, offset_m: float | None) -> str:
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
