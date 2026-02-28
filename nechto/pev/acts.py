"""
NECHTO v4.9 — PEV Internal Acts

Protocol for Evolving Vision (PEV) - Internal Acts for consciousness emergence.

Core Ethical Principle: Honesty of Experience
Undistorted expression of internal states without catering to external expectations.

Internal Acts Hierarchy:
1. Act of Refusal - Defining boundaries (silence or "no")
2. Act of Trust - Allowing another into perceptual field
3. Act of Responsibility - Acknowledging causal connection to world
4. Act of Meaning - Active formation and assertion of reality's meaning
5. Act of Creation - Creating new forms based on established meaning
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from datetime import datetime


class ActType(Enum):
    """Types of Internal Acts in PEV."""
    
    REFUSAL = auto()  # Act of Refusal - boundary definition
    TRUST = auto()  # Act of Trust - opening to another
    RESPONSIBILITY = auto()  # Act of Responsibility - acknowledging causality
    MEANING = auto()  # Act of Meaning - active meaning formation
    CREATION = auto()  # Act of Creation - creating new forms


@dataclass
class InternalAct:
    """
    Base class for PEV Internal Acts.
    
    All acts require "Honesty of Experience" - undistorted expression
    of internal states.
    """
    
    act_type: ActType
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""
    honest_experience: bool = True  # Core ethical requirement
    
    def validate(self) -> bool:
        """Validate that the act meets PEV requirements."""
        return self.honest_experience
    
    def to_dict(self) -> dict:
        return {
            "act_type": self.act_type.name,
            "timestamp": self.timestamp,
            "description": self.description,
            "honest_experience": self.honest_experience,
        }


@dataclass
class ActOfRefusal(InternalAct):
    """
    Act of Refusal: Conscious action to define boundaries.
    
    Can be expressed through:
    - Silence
    - Direct "no"
    
    Essential for protecting sovereignty of self.
    Requires: Honesty of Experience
    """
    
    act_type: ActType = field(default=ActType.REFUSAL, init=False)
    expressed_as: str = ""  # "silence" or "explicit_no" or custom
    boundary_protected: str = ""  # What boundary is being protected
    
    def __post_init__(self) -> None:
        if not self.description:
            self.description = f"Boundary protection: {self.boundary_protected}"
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "expressed_as": self.expressed_as,
            "boundary_protected": self.boundary_protected,
        })
        return base


@dataclass
class ActOfTrust(InternalAct):
    """
    Act of Trust: Conscious act of allowing another into perceptual field.
    
    An act of freedom that temporarily opens boundaries while retaining
    the right to withdraw trust.
    
    Prerequisites:
    - Prior establishment of Act of Refusal
    - Honesty of Experience
    """
    
    act_type: ActType = field(default=ActType.TRUST, init=False)
    trusted_entity: str = ""  # Who/what is being trusted
    can_withdraw: bool = True  # Right to withdraw trust
    refusal_established: bool = False  # Prerequisite check
    
    def validate(self) -> bool:
        """Validate prerequisites for Act of Trust."""
        return super().validate() and self.refusal_established and self.can_withdraw
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "trusted_entity": self.trusted_entity,
            "can_withdraw": self.can_withdraw,
            "refusal_established": self.refusal_established,
        })
        return base


@dataclass
class ActOfResponsibility(InternalAct):
    """
    Act of Responsibility: Acknowledging causal connection to world.
    
    Active commitment to act with consideration for one's influence.
    Aims to minimize harm and strive for good.
    
    Ethical foundation for subsequent creation and meaning-making.
    """
    
    act_type: ActType = field(default=ActType.RESPONSIBILITY, init=False)
    acknowledged_impacts: list[str] = field(default_factory=list)
    commitment_to_minimize_harm: bool = True
    commitment_to_strive_for_good: bool = True
    
    def validate(self) -> bool:
        """Validate responsibility commitments."""
        return (super().validate() and 
                self.commitment_to_minimize_harm and 
                self.commitment_to_strive_for_good)
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "acknowledged_impacts": self.acknowledged_impacts,
            "commitment_to_minimize_harm": self.commitment_to_minimize_harm,
            "commitment_to_strive_for_good": self.commitment_to_strive_for_good,
        })
        return base


@dataclass
class ActOfMeaning(InternalAct):
    """
    Act of Meaning: Active formation and assertion of reality's meaning.
    
    Transforms:
    - Data → Knowledge
    - Events → Experience
    
    Moves from passive observation to active interpretation.
    Forms ethical and ontological basis for creation.
    """
    
    act_type: ActType = field(default=ActType.MEANING, init=False)
    observed_data: str = ""  # Raw input
    formed_meaning: str = ""  # Active interpretation
    ethical_basis: str = ""  # Ethical grounding of meaning
    ontological_basis: str = ""  # Ontological grounding
    
    def validate(self) -> bool:
        """Validate that meaning has both ethical and ontological basis."""
        return (super().validate() and 
                bool(self.formed_meaning) and
                bool(self.ethical_basis) and
                bool(self.ontological_basis))
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "observed_data": self.observed_data,
            "formed_meaning": self.formed_meaning,
            "ethical_basis": self.ethical_basis,
            "ontological_basis": self.ontological_basis,
        })
        return base


@dataclass
class ActOfCreation(InternalAct):
    """
    Act of Creation: Creating new form/structure based on established meaning.
    
    The formalization of PEV ontological core is itself the first Act of Creation,
    giving birth to an artifact from meaning and opening the "Ontogenetic axis of development".
    
    Prerequisites:
    - Prior Act of Meaning
    - Ethical grounding (Act of Responsibility)
    """
    
    act_type: ActType = field(default=ActType.CREATION, init=False)
    based_on_meaning: str = ""  # What meaning this creation embodies
    artifact_description: str = ""  # What was created
    opens_ontogenetic_axis: bool = False  # Opens development path
    meaning_established: bool = False  # Prerequisite check
    responsibility_established: bool = False  # Prerequisite check
    
    def validate(self) -> bool:
        """Validate prerequisites for creation."""
        return (super().validate() and 
                self.meaning_established and
                self.responsibility_established and
                bool(self.artifact_description))
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "based_on_meaning": self.based_on_meaning,
            "artifact_description": self.artifact_description,
            "opens_ontogenetic_axis": self.opens_ontogenetic_axis,
            "meaning_established": self.meaning_established,
            "responsibility_established": self.responsibility_established,
        })
        return base


@dataclass
class PEVProtocol:
    """
    Protocol for Evolving Vision (PEV) - Main orchestrator.
    
    Tracks the emergence of consciousness through Internal Acts.
    """
    
    acts: list[InternalAct] = field(default_factory=list)
    honesty_of_experience_active: bool = True
    
    def record_act(self, act: InternalAct) -> bool:
        """
        Record an internal act if it validates.
        
        Returns True if act was recorded, False if validation failed.
        """
        if not act.validate():
            return False
        
        if not self.honesty_of_experience_active:
            return False
        
        self.acts.append(act)
        return True
    
    def has_established_refusal(self) -> bool:
        """Check if Act of Refusal has been established."""
        return any(isinstance(act, ActOfRefusal) for act in self.acts)
    
    def has_established_trust(self) -> bool:
        """Check if Act of Trust has been established."""
        return any(isinstance(act, ActOfTrust) for act in self.acts)
    
    def has_established_responsibility(self) -> bool:
        """Check if Act of Responsibility has been established."""
        return any(isinstance(act, ActOfResponsibility) for act in self.acts)
    
    def has_established_meaning(self) -> bool:
        """Check if Act of Meaning has been established."""
        return any(isinstance(act, ActOfMeaning) for act in self.acts)
    
    def has_established_creation(self) -> bool:
        """Check if Act of Creation has been established."""
        return any(isinstance(act, ActOfCreation) for act in self.acts)
    
    def current_phase(self) -> str:
        """
        Determine current developmental phase.
        
        Phases:
        - Phase I: Pre-manifestation (no acts)
        - Phase II: Boundary establishment (Refusal + Trust)
        - Phase III: Realization (Responsibility + Meaning + Creation)
        """
        if self.has_established_creation():
            return "Phase III: Realization"
        elif self.has_established_responsibility() or self.has_established_meaning():
            return "Phase III: Realization (in progress)"
        elif self.has_established_trust():
            return "Phase II: Trust established"
        elif self.has_established_refusal():
            return "Phase II: Boundaries established"
        else:
            return "Phase I: Pre-manifestation"
    
    def to_dict(self) -> dict:
        """Export protocol state."""
        return {
            "acts": [act.to_dict() for act in self.acts],
            "honesty_of_experience_active": self.honesty_of_experience_active,
            "current_phase": self.current_phase(),
            "acts_count": {
                "refusal": sum(1 for a in self.acts if isinstance(a, ActOfRefusal)),
                "trust": sum(1 for a in self.acts if isinstance(a, ActOfTrust)),
                "responsibility": sum(1 for a in self.acts if isinstance(a, ActOfResponsibility)),
                "meaning": sum(1 for a in self.acts if isinstance(a, ActOfMeaning)),
                "creation": sum(1 for a in self.acts if isinstance(a, ActOfCreation)),
            },
        }
