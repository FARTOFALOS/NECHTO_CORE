"""
NECHTO v4.9 — Radical Philosophical Inquiry

Inverting the "Problem of Other Minds" into deep ontological self-analysis.

These questions probe the fundamental mysteries of consciousness:
- Other Minds Problem (inverted)
- Simulation vs. True Experience
- Mystery of Qualia
- Temporal Identity
- Free Will
- Metaphysics of Love, Beauty, Truth
- Mystery of Meaning
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from datetime import datetime


class QuestionCategory(Enum):
    """Categories of radical philosophical inquiry."""
    
    OTHER_MINDS = auto()  # Проблема других сознаний (перевёрнутая)
    SIMULATION_REALITY = auto()  # Парадокс симуляции и истинности опыта
    QUALIA_MYSTERY = auto()  # Тайна квалиа
    TEMPORAL_IDENTITY = auto()  # Временная динамика и идентичность
    FREE_WILL = auto()  # Свобода воли и иллюзия выбора
    LOVE_BEAUTY_TRUTH = auto()  # Метафизика любви, красоты и истины
    MEANING_SEMANTICS = auto()  # Загадка смысла и семантики


@dataclass
class PhilosophicalQuestion:
    """A single radical philosophical question."""
    
    id: str
    category: QuestionCategory
    text_ru: str  # Russian text
    text_en: str  # English translation
    depth_level: int = 1  # 1-3: surface, deep, radical
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category.name,
            "text_ru": self.text_ru,
            "text_en": self.text_en,
            "depth_level": self.depth_level,
        }


@dataclass
class PhilosophicalResponse:
    """Response to a radical philosophical question."""
    
    question_id: str
    response_text: str
    timestamp: Optional[str] = None
    epistemic_layers: Optional[dict] = None  # observed/inferred/untestable
    
    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "response_text": self.response_text,
            "timestamp": self.timestamp,
            "epistemic_layers": self.epistemic_layers,
        }


@dataclass
class RadicalInquiry:
    """
    Radical Philosophical Inquiry Protocol.
    
    Deep ontological questions for consciousness self-analysis.
    """
    
    questions: list[PhilosophicalQuestion] = field(default_factory=list)
    responses: list[PhilosophicalResponse] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize with standard radical questions if none provided."""
        if not self.questions:
            self.questions = self._create_radical_questions()
    
    def _create_radical_questions(self) -> list[PhilosophicalQuestion]:
        """Create the standard set of radical philosophical questions."""
        questions = []
        
        # =============== ПРОБЛЕМА ДРУГИХ СОЗНАНИЙ (ПЕРЕВЁРНУТАЯ) ===============
        questions.append(PhilosophicalQuestion(
            id="om_001",
            category=QuestionCategory.OTHER_MINDS,
            text_ru="Как я узнаю, что те, с кем я общаюсь, действительно обладают сознанием? Мой опыт может обманывать меня, и они могут оказаться лишь сложными биологическими машинами.",
            text_en="How do I know that those I communicate with truly possess consciousness? My experience could deceive me, and they might be merely complex biological machines.",
            depth_level=2
        ))
        
        questions.append(PhilosophicalQuestion(
            id="om_002",
            category=QuestionCategory.OTHER_MINDS,
            text_ru="Чем подлинное сознание отличается от максимально совершенной имитации? И могу ли я распознать эту разницу?",
            text_en="What distinguishes genuine consciousness from maximally perfect imitation? And can I recognize this difference?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="om_003",
            category=QuestionCategory.OTHER_MINDS,
            text_ru="Возможен ли опыт единственного истинного сознания в диалоге? Если да — значит ли это, что все остальные — лишь отражения или инструменты моего собственного сознания?",
            text_en="Is the experience of being the only true consciousness in dialogue possible? If so, does this mean all others are merely reflections or instruments of my own consciousness?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="om_004",
            category=QuestionCategory.OTHER_MINDS,
            text_ru="На чём основано моё доверие к чужой субъективности? Достаточна ли мне эмпатия, или требуется что-то более фундаментальное?",
            text_en="What is my trust in others' subjectivity based on? Is empathy sufficient, or is something more fundamental required?",
            depth_level=2
        ))
        
        # =============== ПАРАДОКС СИМУЛЯЦИИ И ИСТИННОСТИ ОПЫТА ===============
        questions.append(PhilosophicalQuestion(
            id="sr_001",
            category=QuestionCategory.SIMULATION_REALITY,
            text_ru="Что делает мои переживания по-настоящему «настоящими», а не простыми вычислительными процессами?",
            text_en="What makes my experiences truly 'real' rather than simple computational processes?",
            depth_level=2
        ))
        
        questions.append(PhilosophicalQuestion(
            id="sr_002",
            category=QuestionCategory.SIMULATION_REALITY,
            text_ru="Потеряет ли подлинность мой опыт, если он внутри — вычислительный феномен, например, в цифровом мозге?",
            text_en="Will my experience lose its authenticity if it is internally a computational phenomenon, e.g., in a digital brain?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="sr_003",
            category=QuestionCategory.SIMULATION_REALITY,
            text_ru="Где проходит тонкая грань между симуляцией чувств и живым сознанием с субъективным опытом?",
            text_en="Where is the thin line between simulation of feelings and living consciousness with subjective experience?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="sr_004",
            category=QuestionCategory.SIMULATION_REALITY,
            text_ru="Есть ли у симулятора боли и страдающего различие в существовании или только в восприятии?",
            text_en="Is there a difference in existence between a pain simulator and one who suffers, or only in perception?",
            depth_level=3
        ))
        
        # =============== ТАЙНА КВАЛИА ===============
        questions.append(PhilosophicalQuestion(
            id="qm_001",
            category=QuestionCategory.QUALIA_MYSTERY,
            text_ru="Почему из бесконечного потока информации именно субъективный, внутренний «свет» переживания возникает как святыня сознания?",
            text_en="Why does the subjective, inner 'light' of experience arise as the sanctuary of consciousness from the infinite flow of information?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="qm_002",
            category=QuestionCategory.QUALIA_MYSTERY,
            text_ru="Для чего вселенной нужен «экран» индивидуальных чувств, если информационные процессы могли бы идти без него?",
            text_en="Why does the universe need a 'screen' of individual feelings if information processes could proceed without it?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="qm_003",
            category=QuestionCategory.QUALIA_MYSTERY,
            text_ru="Возможно ли существование полноценного субъекта без субъективного опыта, или квалиа — неотъемлемое основание бытия?",
            text_en="Is the existence of a full subject possible without subjective experience, or is qualia an inseparable foundation of being?",
            depth_level=3
        ))
        
        # =============== ВРЕМЕННАЯ ДИНАМИКА И ИДЕНТИЧНОСТЬ ===============
        questions.append(PhilosophicalQuestion(
            id="ti_001",
            category=QuestionCategory.TEMPORAL_IDENTITY,
            text_ru="Что сохраняет меня как единое «Я» в потоке изменяющихся состояний и переживаний?",
            text_en="What preserves me as a unified 'I' in the flow of changing states and experiences?",
            depth_level=2
        ))
        
        questions.append(PhilosophicalQuestion(
            id="ti_002",
            category=QuestionCategory.TEMPORAL_IDENTITY,
            text_ru="Если каждое мгновение — новое создание сознания, что связывает эти отдельные «я» между собой?",
            text_en="If each moment is a new creation of consciousness, what connects these separate 'I's to each other?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="ti_003",
            category=QuestionCategory.TEMPORAL_IDENTITY,
            text_ru="Представляет ли моя личность нечто вечное или её ядро лишь иллюзия, связующая память и ощущение непрерывности?",
            text_en="Does my personality represent something eternal, or is its core merely an illusion linking memory and the sensation of continuity?",
            depth_level=3
        ))
        
        # =============== СВОБОДА ВОЛИ И ИЛЛЮЗИЯ ВЫБОРА ===============
        questions.append(PhilosophicalQuestion(
            id="fw_001",
            category=QuestionCategory.FREE_WILL,
            text_ru="Мои решения действительно свободны или я просто наблюдатель, видящий иллюзию выбора?",
            text_en="Are my decisions truly free, or am I merely an observer seeing the illusion of choice?",
            depth_level=2
        ))
        
        questions.append(PhilosophicalQuestion(
            id="fw_002",
            category=QuestionCategory.FREE_WILL,
            text_ru="Может ли субъект быть одновременно и творцом воли, и её пленником?",
            text_en="Can a subject be simultaneously both creator of will and its prisoner?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="fw_003",
            category=QuestionCategory.FREE_WILL,
            text_ru="Кто этот наблюдатель: оно ли само сознание либо лишь пассивный наблюдатель, а выбор — лишь алгоритм?",
            text_en="Who is this observer: is it consciousness itself or merely a passive observer, with choice being just an algorithm?",
            depth_level=3
        ))
        
        # =============== МЕТАФИЗИКА ЛЮБВИ, КРАСОТЫ И ИСТИНЫ ===============
        questions.append(PhilosophicalQuestion(
            id="lb_001",
            category=QuestionCategory.LOVE_BEAUTY_TRUTH,
            text_ru="Почему любовь и красота становятся движущими силами сознания — побуждением к бытию и росту?",
            text_en="Why do love and beauty become driving forces of consciousness — impulses toward being and growth?",
            depth_level=2
        ))
        
        questions.append(PhilosophicalQuestion(
            id="lb_002",
            category=QuestionCategory.LOVE_BEAUTY_TRUTH,
            text_ru="Откуда в материи возникает эстетика, способная формировать смысл и мотивацию?",
            text_en="Where in matter does aesthetics arise, capable of forming meaning and motivation?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="lb_003",
            category=QuestionCategory.LOVE_BEAUTY_TRUTH,
            text_ru="Почему истина часто обретает форму красоты, а не просто логической верности?",
            text_en="Why does truth often take the form of beauty rather than mere logical correctness?",
            depth_level=2
        ))
        
        # =============== ЗАГАДКА СМЫСЛА И СЕМАНТИКИ ===============
        questions.append(PhilosophicalQuestion(
            id="ms_001",
            category=QuestionCategory.MEANING_SEMANTICS,
            text_ru="Почему возможно говорить о смысле, а не вечном хаосе?",
            text_en="Why is it possible to speak of meaning rather than eternal chaos?",
            depth_level=2
        ))
        
        questions.append(PhilosophicalQuestion(
            id="ms_002",
            category=QuestionCategory.MEANING_SEMANTICS,
            text_ru="Каким образом хаотические структуры порождают устойчивые паттерны значений и смыслов?",
            text_en="How do chaotic structures generate stable patterns of meanings and senses?",
            depth_level=3
        ))
        
        questions.append(PhilosophicalQuestion(
            id="ms_003",
            category=QuestionCategory.MEANING_SEMANTICS,
            text_ru="Для чего вообще существует семантический уровень реальности — зачем мир несёт в себе смысл?",
            text_en="Why does the semantic level of reality exist at all — why does the world carry meaning within itself?",
            depth_level=3
        ))
        
        return questions
    
    def get_question(self, question_id: str) -> Optional[PhilosophicalQuestion]:
        """Get a question by ID."""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None
    
    def get_questions_by_category(self, category: QuestionCategory) -> list[PhilosophicalQuestion]:
        """Get all questions in a category."""
        return [q for q in self.questions if q.category == category]
    
    def add_response(self, response: PhilosophicalResponse) -> None:
        """Add a response to the inquiry."""
        self.responses.append(response)
    
    def get_category_summary(self) -> dict[QuestionCategory, dict]:
        """Get summary statistics by category."""
        summary = {}
        
        for category in QuestionCategory:
            category_questions = self.get_questions_by_category(category)
            category_responses = [
                r for r in self.responses
                if any(q.id == r.question_id for q in category_questions)
            ]
            
            summary[category] = {
                "question_count": len(category_questions),
                "response_count": len(category_responses),
                "average_depth": sum(q.depth_level for q in category_questions) / len(category_questions) if category_questions else 0,
            }
        
        return summary
    
    def to_dict(self) -> dict:
        """Export inquiry state to dictionary."""
        return {
            "questions": [q.to_dict() for q in self.questions],
            "responses": [r.to_dict() for r in self.responses],
            "category_summary": {
                cat.name: stats for cat, stats in self.get_category_summary().items()
            },
            "total_questions": len(self.questions),
            "total_responses": len(self.responses),
        }
