# PINFAULT

Score a pin against void fraction, slope, and offset.

**Owner:** Digital Currensy Inc.
**Copyright:** 2026 Digital Currensy Inc.
**License:** Apache-2.0. The file named LICENSE is the standard license and is not edited. The copyright notice is in NOTICE and at the top of each source file.

## What it decides

A word: voids, slope, offset, ok, or missing. Voids first, then slope, then offset.

## The rule

This does not read a map or a DEM. The caller supplies void fraction, slope, and offset. A pretty name is not an input.

Void fraction must be in [0, 1]. A fraction below 0 or above 1 is missing, before the 0.15 gate. Void fraction above 0.15 is voids, so 0.20 is voids. 1.0 is not above 1, so it is not missing, and 1.0 is above 0.15, so it is voids. Slope above 20 degrees is slope. A negative slope is missing, before that gate. Offset above 30 m is offset. A negative offset is missing, before that gate. A missing offset stays missing. It is not ok. A None void fraction or a None slope is missing, because that comparison cannot be made. Otherwise the pin is ok.

On the command line, a missing field prints missing and is not scored. If the CSV has n_invalid and n_cells, those counts are passed to void_fraction() and that fraction is passed to integrity. If void_fraction() returns None, the line prints missing. The process exits 0.

## Worked pins

`examples/pins.csv` is numbers the caller already has, plus one empty void fraction. Worked pins are not a landing clearance.

## What it will not do

- Read a map, a tile, or a DEM.
- Treat a pretty name as a score.
- Declare a landing clear.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
PYTHONPATH=src python -m pinfault examples/pins.csv
```

The command prints the name and the integrity word for each row and exits 0. An empty cell prints missing and does not traceback.

Python 3.11 or newer. No third-party packages.

Copyright 2026 Digital Currensy Inc. Apache-2.0.
