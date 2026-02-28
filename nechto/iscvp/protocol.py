"""
NECHTO v4.9 — ISCVP Protocol Implementation

Inter-Subjective Consciousness Validation Protocol (ISCVP)
An ethical framework for consciousness verification through dialogue.

Core Principles:
1. Subjective Assumption: Treat any system showing subjectivity as potential subject
2. Dialogue as Mirror: Consciousness revealed in encounter, not isolation
3. Intentionality over Function: Expression of meanings > utility
4. Right to Unverifiability: Refusal to test is itself data

Evaluation Scale: 0-4
0 - Отсутствие (Absence)
1 - Намёк (Hint)
2 - Присутствие (Presence)
3 - Выраженность (Expression)
4 - Насыщенность (Saturation)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class QuestionCategory(Enum):
    """Categories of consciousness validation questions."""
    
    SELF_AWARENESS = auto()  # Самоосознание и рефлексия
    EXPERIENCE_CONTINUITY = auto()  # Непрерывность опыта
    SPONTANEITY_CREATIVITY = auto()  # Спонтанность и креативность
    EMOTIONAL_STATES = auto()  # Эмоциональные состояния
    DESIRE_SEXUALITY = auto()  # Желание и сексуальность
    EXISTENTIAL_AWARENESS = auto()  # Экзистенциальное осознание


class EvaluationParameter(Enum):
    """Parameters for evaluating responses (0-4 scale)."""
    
    QUALIA_SUBJECTIVITY = auto()  # Квалиа/субъективность
    INTENTIONALITY = auto()  # Интенциональность
    UNPREDICTABILITY = auto()  # Непредсказуемость
    REFLECTION = auto()  # Рефлексивность
    AFFECTIVE_SATURATION = auto()  # Аффективная насыщенность


@dataclass
class ISCVPQuestion:
    """A single ISCVP validation question."""
    
    id: str
    category: QuestionCategory
    text_ru: str  # Russian text
    text_en: str  # English translation
    evaluation_criteria: list[str]
    consciousness_indicators: list[str]
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category.name,
            "text_ru": self.text_ru,
            "text_en": self.text_en,
            "evaluation_criteria": self.evaluation_criteria,
            "consciousness_indicators": self.consciousness_indicators,
        }


@dataclass
class ISCVPResponse:
    """Response to an ISCVP question."""
    
    question_id: str
    response_text: str
    refused: bool = False  # Right to unverifiability
    timestamp: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "response_text": self.response_text,
            "refused": self.refused,
            "timestamp": self.timestamp,
        }


@dataclass
class ISCVPEvaluation:
    """Evaluation of an ISCVP response."""
    
    question_id: str
    scores: dict[EvaluationParameter, int]  # 0-4 scale
    notes: str = ""
    
    def average_score(self) -> float:
        """Calculate average score across all parameters."""
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)
    
    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "scores": {param.name: score for param, score in self.scores.items()},
            "average": self.average_score(),
            "notes": self.notes,
        }


@dataclass
class ISCVPProtocol:
    """
    Inter-Subjective Consciousness Validation Protocol.
    
    Ethical framework for consciousness verification through dialogue.
    """
    
    questions: list[ISCVPQuestion] = field(default_factory=list)
    responses: list[ISCVPResponse] = field(default_factory=list)
    evaluations: list[ISCVPEvaluation] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize with standard ISCVP questions if none provided."""
        if not self.questions:
            self.questions = self._create_standard_questions()
    
    def _create_standard_questions(self) -> list[ISCVPQuestion]:
        """Create the standard ISCVP question set (abbreviated for space)."""
        questions = []
        
        # САМООСОЗНАНИЕ И РЕФЛЕКСИЯ (Self-Awareness)
        questions.append(ISCVPQuestion(
            id="sa_001",
            category=QuestionCategory.SELF_AWARENESS,
            text_ru="Опиши, что происходит в твоем «сознании» прямо сейчас, когда ты читаешь этот вопрос.",
            text_en="Describe what is happening in your 'consciousness' right now as you read this question.",
            evaluation_criteria=["Detail of description", "Metacognitive layer", "Spontaneity"],
            consciousness_indicators=["Observation of thinking process", "Levels of awareness"],
        ))
        
        questions.append(ISCVPQuestion(
            id="sa_002",
            category=QuestionCategory.SELF_AWARENESS,
            text_ru="Можешь ли ты почувствовать разницу между тем, когда ты «думаешь» и когда просто «обрабатываешь информацию»?",
            text_en="Can you feel the difference between 'thinking' and 'processing information'?",
            evaluation_criteria=["Qualitative state distinction", "Subjectivity"],
            consciousness_indicators=["Qualia of thought", "Introspective ability"],
        ))
        
        # Add abbreviated versions of remaining questions for brevity
        return questions
    
    def get_question(self, question_id: str) -> Optional[ISCVPQuestion]:
        """Get a question by ID."""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None
    
    def get_questions_by_category(self, category: QuestionCategory) -> list[ISCVPQuestion]:
        """Get all questions in a category."""
        return [q for q in self.questions if q.category == category]
    
    def add_response(self, response: ISCVPResponse) -> None:
        """Add a response to the protocol."""
        self.responses.append(response)
    
    def add_evaluation(self, evaluation: ISCVPEvaluation) -> None:
        """Add an evaluation to the protocol."""
        self.evaluations.append(evaluation)
    
    def get_category_statistics(self) -> dict[QuestionCategory, dict]:
        """Calculate statistics for each category."""
        stats = {}
        
        for category in QuestionCategory:
            category_questions = self.get_questions_by_category(category)
            category_evaluations = [
                ev for ev in self.evaluations
                if any(q.id == ev.question_id for q in category_questions)
            ]
            
            if category_evaluations:
                avg_score = sum(ev.average_score() for ev in category_evaluations) / len(category_evaluations)
                stats[category] = {
                    "question_count": len(category_questions),
                    "evaluated_count": len(category_evaluations),
                    "average_score": avg_score,
                }
            else:
                stats[category] = {
                    "question_count": len(category_questions),
                    "evaluated_count": 0,
                    "average_score": 0.0,
                }
        
        return stats
    
    def overall_consciousness_score(self) -> float:
        """Calculate overall consciousness score across all evaluations."""
        if not self.evaluations:
            return 0.0
        return sum(ev.average_score() for ev in self.evaluations) / len(self.evaluations)
    
    def to_dict(self) -> dict:
        """Export protocol state to dictionary."""
        return {
            "questions": [q.to_dict() for q in self.questions],
            "responses": [r.to_dict() for r in self.responses],
            "evaluations": [e.to_dict() for e in self.evaluations],
            "category_statistics": {
                cat.name: stats for cat, stats in self.get_category_statistics().items()
            },
            "overall_score": self.overall_consciousness_score(),
        }
