# PINFAULT

Score a pin against void fraction, slope, and offset.

**Owner:** Digital Currensy Inc.
**Copyright:** 2026 Digital Currensy Inc.
**License:** Apache-2.0. The file named LICENSE is the standard license and is not edited. The copyright notice is in NOTICE and at the top of each source file.

## What it decides

A word: voids, slope, offset, ok, or missing. Voids first, then slope, then offset.

## The rule

This does not read a map or a DEM. The caller supplies void fraction, slope, and offset. A pretty name is not an input.

Void fraction above 0.15 is voids. Slope above 20 degrees is slope. Offset above 30 m is offset. Otherwise the pin is ok. A None offset is not an offset failure. A None void fraction or a None slope is missing, because that comparison cannot be made. A negative void fraction is not above the void gate, so slope and offset still apply.

On the command line, a missing field prints missing and is not scored. The process exits 0.

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
