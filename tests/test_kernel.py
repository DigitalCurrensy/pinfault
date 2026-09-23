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

"""PINFAULT kernel tests. Paper on the pin. Apollo 12 is not this memo."""

from __future__ import annotations

import io
import math
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pinfault.__main__ import main  # noqa: E402
from pinfault.memo import compile_memo  # noqa: E402
from pinfault.score import integrity  # noqa: E402
from pinfault.void_fraction import A11 as A11_VOID  # noqa: E402
from pinfault.void_fraction import CLIP, SIT, void_fraction  # noqa: E402
from pinfault.walk import A11, A12, lunar_offset_m  # noqa: E402


class ScoreTests(unittest.TestCase):
    def test_voids_first(self) -> None:
        self.assertEqual(integrity(0.20, 25, 50), "voids")
        self.assertEqual(integrity(0.15, 2, 400), "offset")
        self.assertEqual(integrity(0.02, 2, 10), "ok")
        self.assertEqual(integrity(0.02, 2, None), "missing")

    def test_none_offset_void_none_or_negative_slope_none(self) -> None:
        self.assertEqual(integrity(0.02, 2, None), "missing")
        self.assertEqual(integrity(None, 2, 10), "missing")
        self.assertEqual(integrity(None, None, None), "missing")
        self.assertEqual(integrity(-0.01, 2, 10), "missing")
        self.assertEqual(integrity(-0.01, 25, 10), "missing")
        self.assertEqual(integrity(-0.01, 2, 40), "missing")
        self.assertEqual(integrity(0.02, None, 10), "missing")
        self.assertEqual(integrity(-0.01, None, 10), "missing")
        self.assertEqual(integrity(0.20, None, None), "voids")
        self.assertEqual(integrity(0.02, 21, None), "slope")

    def test_fraction_in_unit_interval_and_negative_measures(self) -> None:
        self.assertEqual(integrity(0.20, 25, 50), "voids")
        self.assertEqual(integrity(1.0, 25, 50), "voids")
        self.assertEqual(integrity(1.01, 2, 10), "missing")
        self.assertEqual(integrity(0.02, -1.0, 40), "missing")
        self.assertEqual(integrity(0.02, 2, -1.0), "missing")
        self.assertEqual(integrity(0.0, 0.0, 0.0), "ok")


class VoidTests(unittest.TestCase):
    def test_formula(self) -> None:
        self.assertEqual(void_fraction(A11_VOID["n_invalid"], A11_VOID["n_cells"]), 0.02)
        self.assertEqual(void_fraction(CLIP["n_invalid"], CLIP["n_cells"]), 0.20)
        self.assertEqual(void_fraction(SIT["n_invalid"], SIT["n_cells"]), 0.15)
        self.assertIsNone(void_fraction(0, 0))
        self.assertIsNone(void_fraction(-1, 100))
        sit = void_fraction(15, 100)
        assert sit is not None
        self.assertEqual(integrity(sit, 2, 400), "offset")

    def test_nonpositive_cells_or_negative_invalid(self) -> None:
        self.assertIsNone(void_fraction(1, 0))
        self.assertIsNone(void_fraction(1, -3))
        self.assertIsNone(void_fraction(-1, 100))
        self.assertIsNone(void_fraction(-2, -2))


class WalkTests(unittest.TestCase):
    def test_a11_frames(self) -> None:
        self.assertEqual(round(lunar_offset_m((A11["lat"], A11["lon"]), A11["era"])), A11["era_m"])
        self.assertEqual(round(lunar_offset_m((A11["lat"], A11["lon"]), A11["wagner"])), A11["lro_m"])

    def test_a12_named_not_this_memo(self) -> None:
        self.assertEqual(round(lunar_offset_m((A12["lat"], A12["lon"]), A12["era"])), A12["era_m"])
        self.assertEqual(round(lunar_offset_m((A12["lat"], A12["lon"]), A12["wagner"])), A12["lro_m"])
        self.assertFalse(A12["this_memo"])
        self.assertTrue(math.isclose(A12["surveyor_m"], 180))


class MemoTests(unittest.TestCase):
    def test_walk_issues_offset(self) -> None:
        memo = compile_memo("walk")
        self.assertTrue(memo["issued"])
        self.assertEqual(memo["stamp"], "offset")
        self.assertEqual(memo["title"], "PIN MEMO")
        self.assertLessEqual(memo["words"], 80)
        self.assertTrue(memo["do_not_traverse"])
        self.assertTrue(memo["not_a_certificate"])

    def test_voids_and_refused(self) -> None:
        voids = compile_memo("voidclip")
        self.assertTrue(voids["issued"])
        self.assertEqual(voids["stamp"], "voids")
        off = compile_memo("undeclared")
        self.assertFalse(off["issued"])
        self.assertEqual(off["stamp"], "refused")

    def test_a12_refused_okform_other_pin(self) -> None:
        a12 = compile_memo("a12")
        self.assertFalse(a12["issued"])
        self.assertEqual(a12["why"], "not_this_memo")
        self.assertFalse(a12["a12_is_this_memo"])
        ok = compile_memo("okform")
        self.assertTrue(ok["issued"])
        self.assertEqual(ok["stamp"], "ok")
        self.assertNotEqual(ok["pin_id"], A11["id"])


class CliTests(unittest.TestCase):
    def test_pins_csv(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        out = io.StringIO()
        with redirect_stdout(out):
            code = main([str(repo / "examples" / "pins.csv")])
        self.assertEqual(code, 0)
        self.assertEqual(
            out.getvalue().splitlines(),
            ["flat ok", "hole voids", "steep slope", "far offset", "blank missing"],
        )

    def test_counts_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "counts.csv"
            path.write_text(
                "name,n_invalid,n_cells,slope_deg,offset_m\n"
                "hole,20,100,2,10\n"
                "flat,2,100,2,10\n"
                "bad,101,100,2,10\n"
                "full,100,100,2,10\n"
                "neg,-1,100,2,10\n"
                "down,2,100,-3,10\n"
                "left,2,100,2,-4\n",
                encoding="utf-8",
            )
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(path)])
        self.assertEqual(code, 0)
        self.assertEqual(
            out.getvalue().splitlines(),
            [
                "hole voids",
                "flat ok",
                "bad missing",
                "full voids",
                "neg missing",
                "down missing",
                "left missing",
            ],
        )


if __name__ == "__main__":
    unittest.main()
