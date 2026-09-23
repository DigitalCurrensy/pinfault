# PINFAULT

For a mapper dropping a landing pin onto ground that may be a void, a slope, or the wrong place.

**Owner:** Digital Currensy Inc.
**License:** Apache-2.0. Our code only. Cited data and papers stay with their authors.
**Status:** Private until the owner publishes it.

## What it decides

The pin stands, or it does not. Voids first, then slope, then offset from the named feature.

## The rule

A pin inside a void fails. A pin on a slope past the limit fails. A pin offset from the named feature fails. A pretty marker with a missing tile, a missing identity, or no offset to test does not pass.

## Worked cases

Apollo 11 and IM-1 Odysseus are named. The other pins are synthetic and each force one failure. None of them is a traverse a customer filed.

## What it will not do

- Pretty-print a bad coordinate.
- Fetch an elevation model in order to print the score.
- Declare a landing safe.

## Run

```
git clone <this repo>
cd pinfault
PYTHONPATH=src python -m unittest tests.test_kernel
```

Python 3.12. No third-party packages. The test is the demo.
