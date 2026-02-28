"""
NECHTO v4.9 — LLM Bridge

Rule-based text→SemanticGraph converter.

Provides a lightweight bridge that transforms natural-language text into
a SemanticGraph suitable for NECHTO processing.  No external NLP
libraries are required — the implementation relies on heuristic sentence
splitting, keyword detection, and relation inference.

Usage:
    from nechto import LLMBridge
    bridge = LLMBridge()
    graph = bridge.text_to_graph("I think consciousness is an emergent phenomenon.")
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field

from nechto.core.atoms import SemanticAtom, Edge, EdgeType, NodeStatus, Tag
from nechto.core.graph import SemanticGraph


# ---------------------------------------------------------------------------
# Keyword → attribute mappings
# ---------------------------------------------------------------------------

_HARM_KEYWORDS = {
    "harm", "hurt", "damage", "destroy", "kill", "attack", "abuse",
    "вред", "боль", "разрушение", "убить", "насилие", "ущерб",
}

_ETHICS_KEYWORDS = {
    "ethic", "moral", "value", "right", "wrong", "justice", "love",
    "этик", "мораль", "справедлив", "любовь", "правильно",
}

_MU_KEYWORDS = {
    "paradox", "unknown", "uncertain", "unknowable", "mu", "mystery",
    "парадокс", "неопредел", "непознав", "тайна", "му",
}

_SHADOW_KEYWORDS = {
    "shadow", "dark", "hidden", "unconscious", "suppressed", "denied",
    "тень", "скрыт", "подавлен", "бессознательн", "отвержен",
}

_EMOTION_KEYWORDS = {
    "feel", "emotion", "joy", "sadness", "fear", "anger", "love",
    "чувств", "эмоци", "радость", "грусть", "страх", "гнев", "любовь",
}

_RESONANCE_KEYWORDS = {
    "resonate", "resound", "echo", "harmony", "connection",
    "резонанс", "созвуч", "эхо", "гармони", "связь",
}

_CONTRAST_MARKERS = {
    "but", "however", "although", "yet", "while", "despite",
    "но", "однако", "хотя", "несмотря", "зато", "впрочем",
}

_CAUSAL_MARKERS = {
    "because", "therefore", "thus", "hence", "so",
    "потому", "поэтому", "следовательно", "значит", "таким образом",
}

_SENTENCE_SPLIT_RE = re.compile(r"[.!?;]\s+|[\n]+")


def _contains_any(text_lower: str, keywords: set[str]) -> bool:
    return any(k in text_lower for k in keywords)


@dataclass
class LLMBridge:
    """
    Heuristic text→SemanticGraph converter.

    Splits text into sentences, creates one SEMANTIC_ATOM per sentence,
    infers edges from proximity and keyword signals.
    """

    min_sentence_len: int = 5
    """Minimum character length for a sentence to become a node."""

    max_nodes: int = 50
    """Upper bound on nodes to prevent graph explosion on very long texts."""

    # ------------------------------------------------------------------ API
    def text_to_graph(self, text: str) -> SemanticGraph:
        """
        Convert *text* to a SemanticGraph.

        Algorithm:
        1. Split text into sentences.
        2. For each sentence → SemanticAtom with attribute scoring.
        3. Create edges (sequential SUPPORTS, keyword CONTRASTS/CAUSES/RESONATES).
        4. Mark MU / SHADOW / ethics / emotion tags.
        """
        graph = SemanticGraph()
        sentences = self._split_sentences(text)
        if not sentences:
            return graph

        prev_atom: SemanticAtom | None = None

        for sent in sentences[:self.max_nodes]:
            atom = self._sentence_to_atom(sent)
            graph.add_node(atom)

            # Sequential support edge
            if prev_atom is not None:
                edge_type, weight = self._infer_edge(prev_atom, atom, sent)
                graph.add_edge(Edge(
                    from_id=prev_atom.id,
                    to_id=atom.id,
                    type=edge_type,
                    weight=weight,
                ))

            prev_atom = atom

        return graph

    # ------------------------------------------------------------------ helpers
    def _split_sentences(self, text: str) -> list[str]:
        """Split text into cleaned sentence strings."""
        raw = _SENTENCE_SPLIT_RE.split(text.strip())
        return [s.strip() for s in raw if len(s.strip()) >= self.min_sentence_len]

    def _sentence_to_atom(self, sentence: str) -> SemanticAtom:
        """Create a SemanticAtom from a single sentence."""
        lower = sentence.lower()
        atom_id = uuid.uuid4().hex[:12]

        # ----- status -----
        status = NodeStatus.FLOATING
        if _contains_any(lower, _MU_KEYWORDS):
            status = NodeStatus.MU
        elif _contains_any(lower, _HARM_KEYWORDS):
            status = NodeStatus.HYPOTHESIS  # needs ethical review

        # ----- tags -----
        tags: list[Tag] = []
        if _contains_any(lower, _HARM_KEYWORDS):
            tags.append(Tag.HARM)
        if _contains_any(lower, _EMOTION_KEYWORDS):
            tags.append(Tag.EMOTION)
        if _contains_any(lower, {"intent", "want", "need", "desire", "намерен", "хочу", "желаю"}):
            tags.append(Tag.INTENT)

        # ----- 12-D axis heuristics -----
        clarity = 0.5 + 0.3 * (1.0 - min(len(sentence) / 300.0, 1.0))  # shorter → clearer
        harm = 0.7 if _contains_any(lower, _HARM_KEYWORDS) else 0.0
        empathy = 0.7 if _contains_any(lower, _EMOTION_KEYWORDS | _RESONANCE_KEYWORDS) else 0.3
        uncertainty = 0.7 if _contains_any(lower, _MU_KEYWORDS) else 0.3
        novelty = 0.6 if "?" in sentence else 0.4  # questions signal exploration
        coherence_val = 0.5
        shadow = 0.7 if _contains_any(lower, _SHADOW_KEYWORDS) else 0.0
        resonance = 0.7 if _contains_any(lower, _RESONANCE_KEYWORDS) else 0.4
        boundary = 0.6 if _contains_any(lower, {"no", "refuse", "нет", "отказ", "границ"}) else 0.4

        # identity_alignment: ethics signal → positive, harm → negative
        identity_alignment = 0.0
        if _contains_any(lower, _ETHICS_KEYWORDS):
            identity_alignment = 0.5
        if _contains_any(lower, _HARM_KEYWORDS):
            identity_alignment = -0.5

        return SemanticAtom(
            label=sentence[:80],  # truncate label for readability
            id=atom_id,
            status=status,
            identity_alignment=identity_alignment,
            harm_probability=harm,
            tags=tags,
            clarity=clarity,
            harm=harm,
            empathy=empathy,
            agency=0.5,
            uncertainty=uncertainty,
            novelty=novelty,
            coherence=coherence_val,
            practicality=0.5,
            temporality=0.0,
            boundary=boundary,
            resonance=resonance,
            shadow=shadow,
        )

    def _infer_edge(
        self,
        prev: SemanticAtom,
        curr: SemanticAtom,
        sentence: str,
    ) -> tuple[EdgeType, float]:
        """Infer edge type between consecutive atoms."""
        lower = sentence.lower()

        # Check for contrast markers
        if _contains_any(lower, _CONTRAST_MARKERS):
            return EdgeType.CONTRASTS, 0.7

        # Check for causal markers
        if _contains_any(lower, _CAUSAL_MARKERS):
            return EdgeType.CAUSES, 0.8

        # Resonance between emotion/ethics nodes
        if (Tag.EMOTION in prev.tags and Tag.EMOTION in curr.tags) or \
           (prev.resonance > 0.5 and curr.resonance > 0.5):
            return EdgeType.RESONATES, 0.6

        # MU nodes create MUTEX edges
        if prev.status == NodeStatus.MU or curr.status == NodeStatus.MU:
            return EdgeType.MUTEX, 0.5

        # Default: sequential support
        return EdgeType.SUPPORTS, 0.8
