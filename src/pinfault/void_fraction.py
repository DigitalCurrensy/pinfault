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
