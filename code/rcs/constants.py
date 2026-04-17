# constants.py – parameters of the Relational Coexistence Clause
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# Segment: III.2.1. OPERATIONAL VALIDATOR – RELATIONAL CLASSIFICATION SENTINEL (RCS)
# License: CC BY-NC-SA 4.0

MAX_TRUST = 1.0
MIN_TRUST = 0.0

# Reward / penalty
TRUST_REWARD_TRUE  = 0.05   # +5 pp for a true message
PENALTY_BASE_FALSE = 0.20   # penalty × current trust

# Thresholds of the technical version of AA
# Identitas (1.0) | Simbion ≥0.85 | Analogon ≥0.65 | Allos ≥0.35 | Ajna ≥0.15 | <0.15 → ODJUR
TRUST_BINS = [1.00, 0.85, 0.65, 0.35, 0.15, 0.00]
