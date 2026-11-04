"""Energy agent: only proposes steam reduction when the finished product
is within spec. Reducing utilities on off-spec product is forbidden."""


def propose(state: dict) -> list[dict]:
    if not state["overall_quality_ok"]:
        return []
    do = state["units"]["deodorization"]
    current = do["steam_used_kg_per_t"]
    proposed = round(max(20.0, current * 0.97), 2)  # 3% reduction, published baseline
    if proposed >= current:
        return []
    return [{
        "unit": "deodorization",
        "variable": "deod_steam_kg_per_t",
        "current_value": current,
        "proposed_value": proposed,
        "confidence": 0.70,
        "rationale": "quality within spec; 3% steam reduction per published deodorization baseline",
    }]
