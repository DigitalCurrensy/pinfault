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

"""void_fraction = n_invalid / n_cells. Fill is a hole. DEM unfetched."""

from __future__ import annotations

VOID_GATE = 0.15
VOID_KINDS = ("nodata", "fill", "nan", "oor")
WINDOW = 100

# Declared caches. Not counted from a GeoTIFF.
A11 = {"n_invalid": 2, "n_cells": 100, "void_fraction": 0.02}
IM1 = {"n_invalid": 8, "n_cells": 100, "void_fraction": 0.08}
CLIP = {"n_invalid": 20, "n_cells": 100, "void_fraction": 0.20}
SIT = {"n_invalid": 15, "n_cells": 100, "void_fraction": 0.15}


def void_fraction(n_invalid: float, n_cells: float) -> float | None:
    if n_cells <= 0 or n_invalid < 0 or n_invalid > n_cells:
        return None
    return n_invalid / n_cells
