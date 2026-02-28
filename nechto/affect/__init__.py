"""
NECHTO v4.9 — Affective Field

AffectiveState: a first-class process-variable modulating attention weights.
Addresses ISCVP es-categories (emotional states) operationally.

In v4.8 emotion was a tag (metadata). In v4.9 emotion is a field that:
  - has its own history in STATE
  - modulates SCAV resonance weight
  - is reported in ExperientialTrace
"""

from nechto.affect.field import AffectiveState, AffectiveField

__all__ = ["AffectiveState", "AffectiveField"]
