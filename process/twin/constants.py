"""Reference constants for the refining train digital twin.

Values are drawn from published vegetable oil refining literature and
are used here as reasonable order-of-magnitude defaults. Scenario files
in process/twin/scenarios/ override as needed.
"""

# Feedstock: crude soybean oil, typical ranges
FEED_PHOSPHORUS_PPM = 500.0       # crude oil phosphorus, ppm
FEED_FFA_PCT = 0.75               # free fatty acid, %
FEED_COLOR_RED = 12.0             # Lovibond red, crude
FEED_FLOW_TPH = 30.0              # tonnes per hour

# Unit targets (finished oil spec)
TARGET_PHOSPHORUS_PPM = 5.0       # after degumming
TARGET_FFA_PCT = 0.05             # after neutralization/deodorization
TARGET_COLOR_RED = 1.0            # after bleaching
TARGET_TOCOPHEROL_PCT = 0.10      # retain at least 0.10% in deodorization

# Utility baselines (per tonne of oil)
BASELINE_BLEACHING_EARTH_KG_PER_T = 8.0
BASELINE_DEOD_STEAM_KG_PER_T = 25.0
BASELINE_DEOD_TEMP_C = 250.0
BASELINE_DEOD_TIME_MIN = 60.0

# Economic weights (indicative, for advisory ranking)
COST_EARTH_USD_PER_KG = 0.55
COST_STEAM_USD_PER_KG = 0.020
VALUE_QUALITY_PRESERVED_USD_PER_T = 2.50
