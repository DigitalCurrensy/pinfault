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
import sys
from pathlib import Path

from pinfault.score import integrity


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


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python -m pinfault CSV", file=sys.stderr)
        return 2
    with Path(args[0]).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames:
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
        for record in reader:
            name = (record.get("name") or "").strip()
            void = cell(record.get("void_fraction"))
            slope = cell(record.get("slope_deg"))
            offset = cell(record.get("offset_m"))
            if void is None or slope is None or offset is None:
                word = "missing"
            else:
                word = integrity(void, slope, offset)
            print(f"{name} {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
