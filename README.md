# PINFAULT

PINFAULT scores a map pin. A coordinate that looks official can still be the hazard.

**Owner:** Digital Currensy Inc.
**License:** Apache-2.0. Our code only. Cited maps and landings stay with their authors.

## What it decides

The pin stands, or it does not. Voids are checked first, then slope, then the offset from the named feature.

## The rule

A pin inside a void fails. A pin on a slope past the limit fails. A pin offset from the named feature fails. A pretty marker with a missing tile, a missing identity, or no offset to test does not pass.

## Worked cases

The cases in this repository include the Apollo 11 lunar module, IM-1 Odysseus, and a set of synthetic pins that isolate one failure each: flat, void, rim, voids first, a null offset, equal sites, an undeclared identity, and a missing tile. The published pins are named. The synthetic pins are the desk’s own examples. None of them is a traverse a customer filed.

## What it will not do

- Pretty-print a bad coordinate.
- Fetch a digital elevation model in order to print the score.
- Declare a landing safe.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
```

Notes under `docs/` are the build record. This page is the description.
