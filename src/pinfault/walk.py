"""One bad pin. Apollo 11 LM walked. Apollo 12 named, not this memo."""

from __future__ import annotations

import math

MOON_RADIUS_M = 1_737_400

A11 = {
    "id": "PIN-A11-LM",
    "lat": 0.67408,
    "lon": 23.47297,
    "frame": "IAU ME/PA Davies and Colvin 2000",
    "west_m": 400,
    "era": (0.6875, 23.4333),
    "wagner": (0.67416, 23.47314),
    "era_m": 1270,
    "lro_m": 6,
}

A12 = {
    "id": "PIN-A12-LM",
    "lat": -3.01239,
    "lon": -23.42157,
    "frame": "IAU ME/PA Davies and Colvin 2000",
    "site": "Oceanus Procellarum",
    "era": (-3.1975, -23.3856),
    "wagner": (-3.0128, -23.4219),
    "era_m": 5718,
    "lro_m": 16,
    "d87_m": 81,
    "alsep_m": 128,
    "surveyor_m": 180,
    "surveyor_alt_m": 155,
    "head_m": 37,
    "crater_dia_m": 200,
    "this_memo": False,
}


def lunar_offset_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    to_r = math.pi / 180.0
    p1, p2 = a[0] * to_r, b[0] * to_r
    dp = (b[0] - a[0]) * to_r
    dl = (b[1] - a[1]) * to_r
    s = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * MOON_RADIUS_M * math.asin(min(1.0, math.sqrt(s)))
