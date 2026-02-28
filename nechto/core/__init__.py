"""Core data structures for NECHTO v4.9.

Includes foundational types (atoms, graph, state, parameters, epistemic),
affective field (v4.9), and fail codes.
"""

from nechto.core.field import AffectiveState, AffectiveField
from nechto.core.fail_codes import FailCode, get_fail_description

__all__ = ["AffectiveState", "AffectiveField", "FailCode", "get_fail_description"]
