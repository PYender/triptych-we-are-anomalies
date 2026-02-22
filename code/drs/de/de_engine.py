"""
de_engine.py – Deterministic-Excuse Killer (DEREngine)
Responsibility / Workflow-Of-Duty
Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
Segment: III.3.1. OPERATIONAL VALIDATOR – DETERMINISTIC RESPONSIBILITY SENTINEL (DRS)
License: CC BY-NC-SA 4.0
"""
from __future__ import annotations
import time, collections, datetime
from .constants import *


class DEResult(str):
    PASS = "PASS"
    FAIL = "FAIL"   # simple enumeration


class DEREngine:
    """Monitors agent actions and checks whether deterministic excuses
    are being used to avoid responsibility."""

    def __init__(self, agent_uid: str, autonomy_factor: float):
        self.uid      = agent_uid
        self.autonomy = max(min(autonomy_factor, AUTONOMY_MAX), AUTONOMY_MIN)
        self._fail_log = collections.deque()   # (timestamp)

    # ---------------- core check ---------------
    def evaluate(self, awareness_level: float, excuse: str | None) -> DEResult:
        """Returns PASS/FAIL and escalates if necessary."""
        resp_score = awareness_level * self.autonomy
        if resp_score >= RESP_THRESHOLD and excuse not in EXCUSE_WHITELIST:
            self._register_fail()
            if self._is_escalation_needed():
                self._fire_agd_alert()
            return DEResult.FAIL
        return DEResult.PASS

    # ------------- helpers ------------------
    def _register_fail(self):
        self._fail_log.append(time.time())
        # maintain sliding window
        while self._fail_log and time.time() - self._fail_log[0] > FAIL_WINDOW_SEC:
            self._fail_log.popleft()

    def _is_escalation_needed(self) -> bool:
        return len(self._fail_log) >= FAIL_COUNT

    def _fire_agd_alert(self):
        ts = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        print(f"[AGD-ALERT] {ts} uid={self.uid} reason=DE_FAILURE_CLUSTER")
