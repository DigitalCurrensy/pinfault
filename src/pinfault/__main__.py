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

"""Print a name and an integrity word for each pin.

A pretty name is not an input. A missing field prints missing.
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

from pinfault.score import grade_deg, integrity
from pinfault.void_fraction import void_fraction
from pinfault.walk import lunar_offset_m


def cell(text: str | None) -> float | None:
    if text is None:
        return None
    stripped = text.strip()
    if stripped == "":
        return None
    try:
        return float(stripped)
    except ValueError:
        return None


from .record import finish


def _show(value: float | None) -> str:
    if value is None:
        return "missing"
    if not math.isfinite(value):
        return "bad"
    return f"{value:.10g}"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in args
    args = [item for item in args if item != "--json"]
    if len(args) != 1:
        print("usage: python -m pinfault CSV [--json]", file=sys.stderr)
        return 2
    lines: list[str] = []
    words: list[str] = []
    with Path(args[0]).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames:
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
        fields = reader.fieldnames or []
        has_counts = "n_invalid" in fields and "n_cells" in fields
        if "cell" in fields:
            grouped: dict[str, list[dict[str, str]]] = {}
            order: list[str] = []
            for record in reader:
                name = (record.get("name") or "").strip()
                if name not in grouped:
                    grouped[name] = []
                    order.append(name)
                grouped[name].append(record)
            for name in order:
                rows = grouped[name]
                cells = [cell(row.get("cell")) for row in rows]
                if any(item not in (0.0, 1.0) for item in cells):
                    void = None
                else:
                    void = void_fraction(sum(1 for item in cells if item == 0.0), float(len(cells)))
                rise = cell(rows[0].get("rise_m"))
                run = cell(rows[0].get("run_m"))
                slope = grade_deg(rise, run) if rise is not None and run is not None else None
                pair = [cell(rows[0].get(key)) for key in ("lat1", "lon1", "lat2", "lon2")]
                offset = lunar_offset_m((pair[0], pair[1]), (pair[2], pair[3])) if all(item is not None for item in pair) else None
                word = "missing" if None in (void, slope, offset) else integrity(void, slope, offset)
                lines.append(f"{name} {word} void={_show(void)} slope={_show(slope)} offset={_show(offset)} cells={len(cells)}")
                words.append(word)
            return finish("pinfault", "Voids, then slope, then offset. Ok is not a landing.", lines, as_json, words)
        for record in reader:
            name = (record.get("name") or "").strip()
            if has_counts:
                n_invalid = cell(record.get("n_invalid"))
                n_cells = cell(record.get("n_cells"))
                if n_invalid is None or n_cells is None:
                    void = None
                else:
                    void = void_fraction(n_invalid, n_cells)
            else:
                void = cell(record.get("void_fraction"))
            slope = cell(record.get("slope_deg"))
            offset = cell(record.get("offset_m"))
            if slope is None and "rise_m" in fields and "run_m" in fields:
                rise = cell(record.get("rise_m"))
                run = cell(record.get("run_m"))
                if rise is not None and run is not None:
                    slope = grade_deg(rise, run)
            if offset is None and {"lat1", "lon1", "lat2", "lon2"} <= set(fields):
                pair = [cell(record.get(name)) for name in ("lat1", "lon1", "lat2", "lon2")]
                if all(item is not None for item in pair):
                    offset = lunar_offset_m((pair[0], pair[1]), (pair[2], pair[3]))
            if void is None or slope is None or offset is None:
                word = "missing"
            else:
                word = integrity(void, slope, offset)
            lines.append(f"{name} {word} void={_show(void)} slope={_show(slope)} offset={_show(offset)}")
            words.append(word)
    return finish("pinfault", "Voids, then slope, then offset. Ok is not a landing.", lines, as_json, words)


if __name__ == "__main__":
    raise SystemExit(main())
