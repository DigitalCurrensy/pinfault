# PINFAULT

The coordinate everyone trusts may be the thing that kills the traverse.

**Owner:** Digital Currensy Inc.
**Status:** Private. Independent tool. Not a NASA Space Apps 2026 submission.
**License of our code:** Apache-2.0

## One sentence

A pin on a lunar or Mars map looks official. Score it against DEM completeness, slope, named-feature offset, and frame mismatch — or say the pin is not a pin.

## Wave freeze

- W0 catalog: Apollo 11 LM and IM-1 vs declared LOLA/SLDEM tile stats. Scorer named, not run.
- W1 `score.py`: voids > 0.15, else slope > 20, else offset > 30, else ok. Voids first.
- W2 one bad pin: PIN-A11-LM walked. West crater 400 m fails offset. Pretty-print is not a pass.
- W3 memo template: paper on the pin. Offset and voids still issue. Apollo 12 is not this memo.

W4 surveyor pass waits. RIMKEEP locked.

## Void fraction

```
void_fraction = n_invalid / n_cells
```

Invalid is nodata, fill, NaN, or out-of-range elevation. A fill value is a hole, not zero slope. Equality sits. DEM unfetched.

Declared windows: A11 2/100 = 0.02 sits. IM-1 8/100 = 0.08 sits. Operator clip 20/100 = 0.20 trips voids first.

## Apollo 12 is not this memo

Davies-Colvin 2000 −3.01239 / −23.42157. Apollo-era 5718 m off. Wagner 2017 16 m off. Surveyor 3 ~180 m (NASA) / 155 m (LRO article). One coordinate remains PIN-A11-LM.

## What it is not

- Not a pretty-printed pin. Not Google Moon. Not QuickMap as the coordinate.
- Not a live LOLA or SLDEM GeoTIFF GET.
- Not survey-grade. Do not claim a surveyor this wave.
- Not a certificate. Counsel unsigned.
- Not RIMKEEP.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
```
