# Architecture

`src/pinfault/score.py` is the owned scorer. Voids first, then slope, then offset, else ok.

`src/pinfault/void_fraction.py` freezes `n_invalid / n_cells` on a named window. No GeoTIFF GET.

`src/pinfault/walk.py` names Apollo 11 as the walked pin and Apollo 12 as not this memo.

`src/pinfault/memo.py` compiles the paper on the pin. Fail still issues. Refused claim does not.

No live LOLA, SLDEM, SPICE, or MAPTIS. Auth off. URS 1–5 human last.
