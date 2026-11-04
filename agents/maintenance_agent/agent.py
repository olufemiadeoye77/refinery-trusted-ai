"""Maintenance agent: revises remaining-useful-life estimates for
bleaching filter sleeves based on earth loading. Advisory only."""


def propose(state: dict) -> list[dict]:
    earth = state["utilities"]["bleaching_earth_kg_per_t"]
    if earth < 10.0:
        return []
    return [{
        "unit": "bleaching",
        "variable": "bleaching_filter_rul_hours",
        "current_value": 240.0,
        "proposed_value": 180.0,
        "confidence": 0.65,
        "rationale": f"earth loading {earth} kg/t elevated; RUL revised down 25%",
    }]
