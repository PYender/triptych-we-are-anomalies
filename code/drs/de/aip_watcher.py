"""
aip_watcher.py – AIP-Watcher v1.2
Computes awareness_level from four signal streams:
  (self-report, behaviour entropy, narrative colour, system_tension)
  awareness_level = 0…1 (prop, rolling 1 min)

Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
Segment: III.3.1. OPERATIONAL VALIDATOR – DETERMINISTIC RESPONSIBILITY SENTINEL (DRS)
License: CC BY-NC-SA 4.0
"""
import numpy as np
import pandas as pd


class AIPWatcher:
    def __init__(self, window_sec: int = 60):
        self.window = window_sec
        self.buffer = []

    def push_sample(self, self_report: float,
                    behaviour_entropy: float,
                    narrative_colour: float,
                    system_tension: float):
        """Each signal in the 0–1 range (tension inverted)."""
        score = np.mean([
            self_report,
            behaviour_entropy,
            1 - narrative_colour,   # red — lower awareness
            1 - system_tension      # high tension lowers awareness
        ])
        ts = pd.Timestamp.utcnow()
        self.buffer.append((ts, score))
        # trim window
        self.buffer = [(t, s) for t, s in self.buffer
                       if (ts - t).total_seconds() <= self.window]

    @property
    def awareness_level(self) -> float:
        if not self.buffer:
            return 0.0
        return float(np.mean([s for _, s in self.buffer]))
