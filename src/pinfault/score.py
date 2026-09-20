def integrity(void_fraction: float, slope_deg: float, offset_m: float | None) -> str:
    if void_fraction > 0.15:
        return "voids"
    if slope_deg > 20:
        return "slope"
    if offset_m is not None and offset_m > 30:
        return "offset"
    return "ok"
