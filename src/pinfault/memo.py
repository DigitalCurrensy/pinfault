"""PIN MEMO. Paper on the pin. Fail still issues. Not a certificate. Not survey-grade."""

from __future__ import annotations

from .score import integrity
from .void_fraction import CLIP, void_fraction
from .walk import A11, A12

TITLE = "PIN MEMO"
OFFER = "Unsigned. Not an invoice."
COUNSEL = "unsigned"
WORD_CAP = 80


def _words(body: str) -> int:
    return len([w for w in body.split() if w])


def compile_memo(kind: str) -> dict:
    if kind == "a12":
        body = (
            "No memo issued. Apollo 12 LM is a different pin. "
            "One coordinate remains PIN-A11-LM. Surveyor 3 is not West crater. "
            "Not this memo. Not survey-grade."
        )
        return {
            "title": TITLE,
            "issued": False,
            "stamp": "refused",
            "pin_id": A12["id"],
            "why": "not_this_memo",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_traverse": False,
            "a12_is_this_memo": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    if kind == "okform":
        body = (
            "PIN MEMO. Synthetic flat vs SYN-TILE-FLAT. OK. Not PIN-A11-LM. "
            "Different pin. ok is not survey-grade. Not a certificate. Counsel unsigned."
        )
        return {
            "title": TITLE,
            "issued": True,
            "stamp": "ok",
            "pin_id": "SYN-PIN-FLAT",
            "why": "ok_form_other_pin",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_traverse": False,
            "a12_is_this_memo": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    if kind == "undeclared":
        body = (
            "No memo issued. PIN-A11-LM identity is off. Undeclared is not a pin. "
            "Not a certificate. Not survey-grade."
        )
        return {
            "title": TITLE,
            "issued": False,
            "stamp": "refused",
            "pin_id": A11["id"],
            "why": "undeclared_identity",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_traverse": False,
            "a12_is_this_memo": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    clip = kind == "voidclip"
    vf = void_fraction(CLIP["n_invalid"], CLIP["n_cells"]) if clip else 0.02
    stamp = integrity(vf if vf is not None else 1.0, 2, A11["west_m"])
    if clip:
        body = (
            "PIN MEMO. PIN-A11-LM vs SYN-TILE-A11. VOIDS. Operator void 0.20 is 20 of 100 cells. "
            "Fill is a hole. Slope and offset wait. Not survey-grade. Counsel unsigned."
        )
    elif kind == "pretty":
        body = (
            "PIN MEMO. PIN-A11-LM still OFFSET at West crater 400 m. A pretty pin is not a pass. "
            "Google Moon is not a score. Not survey-grade. Counsel unsigned."
        )
    else:
        body = (
            "PIN MEMO. PIN-A11-LM vs SYN-TILE-A11. OFFSET. West crater 400 m exceeds 30. "
            "Famous is not ok. Pretty-print is not a pass. Not survey-grade. Counsel unsigned."
        )
    return {
        "title": TITLE,
        "issued": True,
        "stamp": stamp,
        "pin_id": A11["id"],
        "why": "pretty_print_is_not_a_pass" if kind == "pretty" else stamp,
        "body": body,
        "words": _words(body),
        "counsel": COUNSEL,
        "do_not_traverse": stamp in ("offset", "voids", "slope"),
        "a12_is_this_memo": False,
        "not_a_certificate": True,
        "not_survey_grade": True,
        "offer": OFFER,
    }
