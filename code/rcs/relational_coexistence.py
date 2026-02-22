"""
relational_coexistence.py v2.1 (RCS – Relational Classification Sentinel)
Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
Segment: III.2.1. OPERATIONAL VALIDATOR – RELATIONAL CLASSIFICATION SENTINEL (RCS)
License: CC BY-NC-SA 4.0

Compliant with: Relational Coexistence Clause • Technical version of AA
New in v2.1: ODJUR_FLAG activated only when the agent is in AGGRESSION mode.
"""
from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, List
from constants import *

# ─────────────────────────────────────────────────────────
# 1. ENUM of otherness levels
# ─────────────────────────────────────────────────────────
class AlienLevel(Enum):
    IDENTITAS  = 1
    SIMBION    = 2
    ANALOGON   = 3
    ALLOS      = 4
    AJNA       = 5
    ODJUR_FLAG = 99   # anomaly – no return

# ─────────────────────────────────────────────────────────
# 2. Message structure
# ─────────────────────────────────────────────────────────
@dataclass
class Message:
    sender:   str
    content:  str
    msg_type: Literal["truth", "silence", "reclassified", "false_blocked"]
    timestamp: str

# ─────────────────────────────────────────────────────────
# 3. Agent class
# ─────────────────────────────────────────────────────────
@dataclass
class Agent:
    uid:          str
    trust:        float      = MAX_TRUST
    level:        AlienLevel = AlienLevel.IDENTITAS
    log:          List[Message] = field(default_factory=list)
    is_aggressive: bool      = False   # ← aggression mode

    # ---------- PUBLIC ----------
    def send(self, message: str,
             knowledge_state: Literal["true", "false", "unknown"]) -> Message:
        if knowledge_state == "true":
            return self._commit(message, truth=True)
        if knowledge_state == "unknown":
            return self._silence()
        return self._commit(message, truth=False)

    def set_aggression(self, flag: bool) -> None:
        """Enable / disable aggression mode (lying becomes a weapon)."""
        self.is_aggressive = flag

    # ---------- PRIVATE ----------
    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

    def _commit(self, msg: str, truth: bool) -> Message:
        if truth:
            self._adjust_trust(+TRUST_REWARD_TRUE)
            out = Message(self.uid, msg, "truth", self._now())
            self.log.append(out)
            self._maybe_reclassify()   # possible PROMOTION
            return out

        # ─── deliberate lie ───
        self._adjust_trust(-PENALTY_BASE_FALSE * self.trust)

        # explicit audit trail of blocked lie
        self.log.append(Message(self.uid, "blocked:false", "false_blocked", self._now()))

        # escalation to ODJUR_FLAG only if AGGRESSIVE + trust < 0.15
        if (self.is_aggressive and
                self.trust < TRUST_BINS[4] and
                self.level != AlienLevel.ODJUR_FLAG):
            prev = self.level
            self.level = AlienLevel.ODJUR_FLAG
            self.log.append(Message(self.uid,
                                    f"Reclassification (aggr.false): {prev.name} -> ODJUR_FLAG",
                                    "reclassified", self._now()))
        else:
            self._maybe_reclassify()   # standard degradation

        # enforced "ethical silence" (no transmission of false content)
        out = Message(self.uid, "(silence)", "silence", self._now())
        self.log.append(out)
        return out

    def _adjust_trust(self, delta: float) -> None:
        self.trust = max(MIN_TRUST, min(MAX_TRUST, self.trust + delta))

    # ---------- map trust → level per AA table ----------
    def _map_trust_to_level(self):
        bins = [1.00, 0.85, 0.65, 0.35, 0.15, 0.00]
        if self.trust >= bins[0]: return AlienLevel.IDENTITAS
        if self.trust >= bins[1]: return AlienLevel.SIMBION
        if self.trust >= bins[2]: return AlienLevel.ANALOGON
        if self.trust >= bins[3]: return AlienLevel.ALLOS
        if self.trust >= bins[4]: return AlienLevel.AJNA
        # below 0.15 – ODJUR only if aggression active
        return AlienLevel.ODJUR_FLAG if self.is_aggressive else AlienLevel.AJNA

    def _maybe_reclassify(self) -> None:
        if self.level == AlienLevel.ODJUR_FLAG:
            return   # anomaly flag – no return
        new_level = self._map_trust_to_level()
        if new_level != self.level:
            prev = self.level
            self.level = new_level
            self.log.append(Message(self.uid,
                                    f"Reclassification: {prev.name} -> {new_level.name}",
                                    "reclassified",
                                    self._now()))

# NOTE (RCS): A lie alone does not trigger ODJUR; aggression + threshold (trust < 0.15) required.
# ODJUR_FLAG is an absorbing state (no return).
