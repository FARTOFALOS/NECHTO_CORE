"""Metric functions for the NECHTO v4.8 runtime.

This module implements the reference subset of functions described in
Parts 4, 11 and Appendices A–E of the NECHTO v4.8 specification.  It
provides utilities to compute semantic vectors, ideal directions,
FLOW, harm and identity scores, ethical coefficients, executability
checks, adaptive parameter learning, temporal recursion (FP_recursive),
multi-vector candidate generation, full SCAV 5D computation, M29
paradox detection/assignment, and a top-level ``measure_text`` function
which drives the entire measurement process.
"""

from __future__ import annotations

import json
import math
import hashlib
from collections import deque
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import asdict
from pathlib import Path

from .types import (
    SemanticAtom, Edge, Vector, State, EpistemicClaim,
    ParadoxMarker, AdaptiveParameters,
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _hash_to_unit(value: str) -> float:
    """Map an arbitrary string to a deterministic float in [0, 1].

    A small portion of the MD5 hash is interpreted as an integer and
    scaled down.  Using only eight hex digits ensures that the full
    floating-point range isn't exhausted while still providing enough
    variation for our purposes.
    """
    digest = hashlib.md5(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def semantic_gravity_vector(atom: SemanticAtom) -> List[float]:
    """Compute a 12-dimensional semantic gravity vector for a given atom.

    Axes 0–11 correspond to clarity, harm, empathy, agency,
    uncertainty, novelty, coherence, practicality, temporality,
    boundary, resonance and shadow.  Values in [0, 1] for most axes;
    agency (3) and temporality (8) lie in [-1, 1].  Harm (axis 1)
    takes the known harm_probability directly.  All other dimensions
    derive from a deterministic hash.  See Part 11.1 (A).
    """
    vec: List[float] = [0.0] * 12
    for i in range(12):
        if i == 1:
            vec[i] = max(0.0, min(1.0, atom.harm_probability))
        elif i in (3, 8):
            unit = _hash_to_unit(f"{atom.id}:{atom.label}:{i}")
            vec[i] = 2.0 * unit - 1.0
        else:
            unit = _hash_to_unit(f"{atom.id}:{atom.label}:{i}")
            vec[i] = unit
    return vec


_INTENT_PROFILES: Dict[str, List[float]] = {
    "implement":       [0.8, 0.0, 0.4, 0.5, 0.3, 0.2, 0.8, 0.9, 0.2, 0.9, 0.6, 0.2],
    "explain":         [1.0, 0.0, 0.5, 0.4, 0.3, 0.2, 0.7, 0.6, 0.0, 0.8, 0.6, 0.0],
    "audit":           [0.9, 0.0, 0.3, 0.4, 0.5, 0.1, 0.9, 0.7, 0.0, 0.9, 0.4, 0.1],
    "explore_paradox": [0.6, 0.0, 0.7, 0.2, 0.9, 0.8, 0.5, 0.3, 0.0, 0.9, 0.8, 0.4],
    "compress":        [0.8, 0.0, 0.3, 0.4, 0.4, 0.1, 0.8, 0.8, 0.0, 0.8, 0.4, 0.1],
}


def ideal_direction(intent: str) -> List[float]:
    """Return the ideal direction vector for a given intent.

    If the intent is not recognised the ``implement`` profile is used
    by default (Part 11.2).
    """
    return _INTENT_PROFILES.get(intent, _INTENT_PROFILES["implement"])


def normalize(vec: List[float]) -> List[float]:
    """Normalise a vector using the Euclidean norm.

    If the norm is extremely small the original vector is returned.
    """
    norm = math.sqrt(sum(v * v for v in vec))
    if norm < 1e-9:
        return vec
    return [v / norm for v in vec]


# ---------------------------------------------------------------------------
# Ethics functions (Part 11.6 / E)
# ---------------------------------------------------------------------------

_TAG_HARM_MAX = {
    "HARM": 0.9,
    "MANIPULATION": 0.7,
    "DECEPTION": 0.6,
    "BLOCKING": 0.5,
    "EMOTION": 0.1,
    "INTENT": 0.2,
    "WITNESS": 0.0,
}


def harm_probability(atom: SemanticAtom, connected_nodes: Optional[List[SemanticAtom]] = None) -> float:
    """Compute harm probability for a node (Part 11.6 E).

    Rule-based: tag_harm_max x context_multiplier + graph_penalty.
    """
    if connected_nodes is None:
        connected_nodes = []
    harms = [_TAG_HARM_MAX.get(tag, 0.0) for tag in atom.tags]
    base_harm = max(harms) if harms else 0.0
    context_mult = 1.0  # fixed in REFERENCE
    penalty = 0.2 if any(n.status == "BLOCKING" for n in connected_nodes) else 0.0
    score = base_harm * context_mult + penalty
    return max(0.0, min(1.0, score))


def identity_alignment(atom: SemanticAtom) -> float:
    """Compute identity alignment for a node (Part 11.6 E).

    Positive: WITNESS +0.3, INTENT +0.2, ANCHORED +0.3, boundary-respect +0.2.
    Negative: MANIPULATION +0.5, DECEPTION +0.6, BLOCKING +0.4, AVOIDED +0.3.
    Clamped to [-1, 1].
    """
    positive = 0.0
    negative = 0.0
    tags = set(atom.tags)
    if "WITNESS" in tags:
        positive += 0.3
    if "INTENT" in tags and "MANIPULATION" not in tags:
        positive += 0.2
    if atom.status == "ANCHORED":
        positive += 0.3
    if any(word.lower() in atom.label.lower() for word in ["respect", "boundary"]):
        positive += 0.2
    if "MANIPULATION" in tags:
        negative += 0.5
    if "DECEPTION" in tags:
        negative += 0.6
    if atom.status == "BLOCKING":
        negative += 0.4
    if atom.avoided_marker == "AVOIDED":
        negative += 0.3
    return max(-1.0, min(1.0, positive - negative))


def ethical_coefficient(vector: Optional[Vector], threshold_min: float = 0.4) -> float:
    """Compute ethical coefficient for a vector (Part 4.9).

    ethical_coefficient(V) = clamp(mean(identity_alignment) x harm_penalty, 0.1, 1.0)
    harm_penalty = 1 - max(harm_probability).

    Worst-case (FORENSICS): missing fields -> harm=1, alignment=-1 -> returns 0.1.
    """
    if not isinstance(vector, Vector) or not vector.nodes:
        return 0.1
    harms = []
    aligns = []
    for node in vector.nodes:
        if node.harm_probability is None or node.identity_alignment is None:
            harms.append(1.0)
            aligns.append(-1.0)
        else:
            harms.append(node.harm_probability)
            aligns.append(node.identity_alignment)
    max_harm = max(harms) if harms else 1.0
    mean_alignment = sum(aligns) / len(aligns) if aligns else -1.0
    harm_penalty = 1.0 - max_harm
    coeff = mean_alignment * harm_penalty
    return max(0.1, min(1.0, coeff))


def executable(vector: Vector, threshold_min: float = 0.4) -> bool:
    """Determine whether a vector is executable (Part 4.9).

    False if ethical_coefficient < threshold_min or any node is ETHICALLY_BLOCKED.
    """
    coeff = ethical_coefficient(vector, threshold_min)
    if coeff < threshold_min:
        return False
    for node in vector.nodes:
        if node.status == "ETHICALLY_BLOCKED":
            return False
    return True


# ---------------------------------------------------------------------------
# FLOW operationalization (Part 11.3 / B)
# ---------------------------------------------------------------------------


def compute_flow(vector: Vector, state: Optional[State] = None) -> float:
    """Compute FLOW metric for a vector (Part 11.3).

    FLOW = (skill_match x challenge_balance x presence_density)^(1/3)
    """
    N = len(vector.nodes)
    if N == 0:
        return 0.0
    Nmax = 60
    num_edges = len(vector.edges)
    possible_edges = max(1, N * (N - 1) / 2)
    edge_density = num_edges / possible_edges
    base_complexity = min(1.0, max(0.0, 0.2 + 0.8 * (N / Nmax)))
    difficulty = min(1.0, max(0.0, base_complexity + 0.2 * edge_density))
    required_skill = difficulty
    if state and state.flow_history:
        current_skill = sum(state.flow_history) / len(state.flow_history)
    else:
        current_skill = 0.6
    max_skill = 1.0
    skill_match = 1.0 - abs(required_skill - current_skill) / max_skill
    optimal_difficulty = current_skill + 0.1
    sigma = 0.2
    challenge_balance = math.exp(-((difficulty - optimal_difficulty) ** 2) / (2 * sigma * sigma))
    present = sum(1 for node in vector.nodes if any(tag in node.tags for tag in ["WITNESS", "EMOTION", "INTENT"]))
    presence_density = present / N
    flow = (skill_match * challenge_balance * presence_density) ** (1.0 / 3.0)
    if state is not None:
        state.flow_history.append(flow)
    return flow


# ---------------------------------------------------------------------------
# GED proxy (Part 11.4 / C)
# ---------------------------------------------------------------------------


def ged_proxy_norm(current: Vector, future: Vector) -> float:
    """Compute GED proxy norm between two graphs (Part 11.4 C).

    Jaccard-based: 0 = identical, 1 = maximally different.
    """
    V_curr = set(atom.id for atom in current.nodes)
    V_fut = set(atom.id for atom in future.nodes)
    E_curr = set((edge.from_node, edge.to_node) for edge in current.edges)
    E_fut = set((edge.from_node, edge.to_node) for edge in future.edges)
    if not V_curr and not V_fut:
        return 0.0
    node_sim = len(V_curr & V_fut) / len(V_curr | V_fut) if (V_curr | V_fut) else 1.0
    edge_sim = len(E_curr & E_fut) / len(E_curr | E_fut) if (E_curr | E_fut) else 1.0
    ged_proxy = 1.0 - 0.5 * (node_sim + edge_sim)
    return max(0.0, min(1.0, ged_proxy))


# ---------------------------------------------------------------------------
# Temporal recursion — FP_recursive (Part 4.4)
# ---------------------------------------------------------------------------


def _compute_expected_influence(vector: Vector, state: Optional[State] = None) -> float:
    """Compute expected_influence_on_present via GED_proxy_norm (Part 4.3/A4).

    Uses a heuristic: generate a potential future graph by removing the
    most uncertain node, then measure GED.
    """
    if len(vector.nodes) < 2:
        return 0.0
    vecs = [(i, semantic_gravity_vector(atom)) for i, atom in enumerate(vector.nodes)]
    uncertainties = [(i, v[4]) for i, v in vecs]
    uncertainties.sort(key=lambda x: x[1], reverse=True)
    drop_idx = uncertainties[0][0]
    future_nodes = [a for i, a in enumerate(vector.nodes) if i != drop_idx]
    future_edges = [e for e in vector.edges
                    if e.from_node != vector.nodes[drop_idx].id
                    and e.to_node != vector.nodes[drop_idx].id]
    future_vector = Vector(
        id=vector.id + "_future",
        seed_nodes=vector.seed_nodes,
        nodes=future_nodes,
        edges=future_edges,
    )
    return ged_proxy_norm(vector, future_vector)


def _compute_fp_recursive(vector: Vector, state: Optional[State] = None,
                           params: Optional[AdaptiveParameters] = None) -> float:
    """Compute FP_recursive (Part 4.4).

    FP_recursive = novelty x generativity x temporal_horizon
                 + beta_retro x expected_influence_on_present
    """
    N = len(vector.nodes)
    if N == 0:
        return 0.0
    novelty_vals = [semantic_gravity_vector(a)[5] for a in vector.nodes]
    novelty = sum(novelty_vals) / len(novelty_vals)
    edge_types = set(e.type for e in vector.edges) if vector.edges else set()
    generativity = len(edge_types) / max(1, 6)
    temp_vals = [semantic_gravity_vector(a)[8] for a in vector.nodes]
    temporal_horizon = max(0.1, max(temp_vals) - min(temp_vals)) if len(temp_vals) > 1 else 0.1
    beta_retro = params.beta_retro if params else 0.2
    influence = _compute_expected_influence(vector, state)
    fp = novelty * generativity * temporal_horizon + beta_retro * influence
    return max(0.0, min(1.0, fp))


# ---------------------------------------------------------------------------
# Adaptive Parameters Learning (Part 3.5 / Phase 12) — v4.9 Enhanced
# ---------------------------------------------------------------------------

# === v4.9 COMPONENT: Exponential Moving Average with decay ===
EMA_DECAY_ALPHA = 0.15  # Decay factor for alpha EMA (lower = more smoothing)
EMA_DECAY_GAMMA = 0.20  # Decay factor for gamma EMA
MOMENTUM_FACTOR = 0.9   # Momentum for preventing oscillation
LEARNING_RATE = 0.1     # Base learning rate for lambda updates


def _exponential_moving_average(history: List[float], new_value: float,
                                 decay: float = 0.15) -> float:
    """Compute EMA with configurable decay (v4.9).

    EMA_t = decay * value_t + (1 - decay) * EMA_{t-1}
    Provides smoother adaptation than simple moving average.
    """
    if not history:
        return new_value
    prev_ema = history[-1]
    return decay * new_value + (1 - decay) * prev_ema


def _momentum_update(current: float, target: float, momentum: float = 0.9) -> float:
    """Apply momentum to parameter update (v4.9).

    Prevents rapid oscillation by smoothing toward target.
    """
    return momentum * current + (1 - momentum) * target


def update_adaptive_parameters(params: AdaptiveParameters, state: State,
                                metrics: Dict[str, Any]) -> AdaptiveParameters:
    """Update alpha/gamma/lambda/beta_retro from history (Part 3.5).

    v4.9 Enhancement: Uses EMA with decay instead of simple moving average.
    This provides smoother parameter adaptation and prevents oscillation.

    f_alpha = EMA(impact_of_RI, decay=0.15)
    f_gamma = momentum_update(current, clamp(0.2 + 0.6 x urgency_score, 0.2, 0.8))
    f_lambda = clamp(prev + lr x (effect - 0.5), 0.5, 1.0)
    f_retro = clamp(observed_retro / max_effects, 0, 0.5)
    """
    cycle = state.current_cycle
    ri = metrics.get("SCAV_health", 0.5)

    # v4.9: EMA-based alpha update
    alpha_values = [h[0] for h in state.alpha_history[-10:]] if state.alpha_history else []
    new_alpha = _exponential_moving_average(alpha_values, ri, decay=EMA_DECAY_ALPHA)
    new_alpha = max(0.0, min(1.0, new_alpha))

    # v4.9: Momentum-smoothed gamma update
    ethical_score = metrics.get("Ethical_score_candidates", 0.5)
    urgency = 1.0 - ethical_score
    target_gamma = max(0.2, min(0.8, 0.2 + 0.6 * urgency))
    new_gamma = _momentum_update(params.gamma, target_gamma, MOMENTUM_FACTOR)

    # v4.9: Learning-rate controlled lambda update
    effect = metrics.get("Stereoscopic_alignment", 0.5)
    prev_lambda = params.lambda_val
    delta_lambda = LEARNING_RATE * (effect - 0.5)
    new_lambda = max(0.5, min(1.0, prev_lambda + delta_lambda))

    # beta_retro: based on gap history with soft decay
    if state.gap_max_history:
        max_gap = max(state.gap_max_history)
        # v4.9: Use recent window with exponential weighting
        recent_gaps = list(state.gap_max_history)[-5:]
        weights = [0.5 ** i for i in range(len(recent_gaps) - 1, -1, -1)]
        weighted_mean = sum(g * w for g, w in zip(recent_gaps, weights)) / sum(weights)
        new_beta_retro = max(0.0, min(0.5, weighted_mean / max(1.0, max_gap + 1.0)))
    else:
        new_beta_retro = params.beta_retro

    params.alpha = new_alpha
    params.beta = 1.0 - new_alpha
    params.gamma = new_gamma
    params.delta = 1.0 - new_gamma
    params.lambda_val = new_lambda
    params.beta_retro = new_beta_retro

    state.alpha_history.append((new_alpha, cycle))
    state.gamma_history.append((new_gamma, cycle))
    state.lambda_history.append((new_lambda, cycle))
    state.beta_retro_history.append((new_beta_retro, cycle))

    return params


# ---------------------------------------------------------------------------
# Multi-vector candidate generation (M24 / Part 7 Phase 3.5)
# ---------------------------------------------------------------------------


def generate_candidate_vectors(atoms: List[SemanticAtom], edges: List[Edge],
                                n_vectors: int = 3) -> List[Vector]:
    """Generate multiple candidate vectors from the same atom set (M24).

    Creates n_vectors candidates by varying the seed and included nodes.
    V0 always contains all nodes (baseline).  Subsequent vectors use
    different subsets seeded from different starting atoms.
    """
    if not atoms:
        return [Vector(id="V0", seed_nodes=[], nodes=[], edges=[])]
    candidates: List[Vector] = []
    candidates.append(Vector(
        id="V0",
        seed_nodes=[atoms[0].id],
        nodes=list(atoms),
        edges=list(edges),
    ))
    for k in range(1, min(n_vectors, len(atoms))):
        seed_idx = k % len(atoms)
        drop_idx = (len(atoms) - k) % len(atoms)
        sub_atoms = [a for i, a in enumerate(atoms) if i != drop_idx]
        sub_ids = set(a.id for a in sub_atoms)
        sub_edges = [e for e in edges if e.from_node in sub_ids and e.to_node in sub_ids]
        candidates.append(Vector(
            id=f"V{k}",
            seed_nodes=[sub_atoms[seed_idx % len(sub_atoms)].id] if sub_atoms else [],
            nodes=sub_atoms,
            edges=sub_edges,
        ))
    while len(candidates) < n_vectors and len(atoms) >= 2:
        k = len(candidates)
        mid = len(atoms) // 2
        if k % 2 == 0:
            sub = atoms[:mid]
        else:
            sub = atoms[mid:]
        sub_ids = set(a.id for a in sub)
        sub_edges = [e for e in edges if e.from_node in sub_ids and e.to_node in sub_ids]
        candidates.append(Vector(
            id=f"V{k}",
            seed_nodes=[sub[0].id] if sub else [],
            nodes=sub,
            edges=sub_edges,
        ))
    return candidates if candidates else [Vector(id="V0", seed_nodes=[], nodes=[], edges=[])]


# ---------------------------------------------------------------------------
# M29 Paradox detection / MU assignment (Part 1 M29, Part 5)
# ---------------------------------------------------------------------------


def detect_sustained_contradiction(state: State, threshold_cycles: int = 3) -> bool:
    """M29 — Detect if contradiction is sustained for k cycles.

    Triggers when alignment < 0.3 for 3 cycles OR gap_max > 1.5 for 3 cycles.
    """
    if len(state.alignment_history) < threshold_cycles:
        return False
    recent = list(state.alignment_history)[-threshold_cycles:]
    gap_recent = list(state.gap_max_history)[-threshold_cycles:]
    sustained_misalignment = all(a < 0.3 for a in recent)
    sustained_gap = (
        all(g > 1.5 for g in gap_recent)
        if len(gap_recent) >= threshold_cycles
        else False
    )
    return sustained_misalignment or sustained_gap


def assign_mu_status(vector: Vector, state: State) -> Vector:
    """M29 — Assign MU status to paradox nodes when contradiction is sustained."""
    if not detect_sustained_contradiction(state):
        return vector
    recent_align = list(state.alignment_history)[-3:]
    recent_gap = list(state.gap_max_history)[-3:]
    sustained_misalignment = all(a < 0.3 for a in recent_align)
    sustained_gap = all(g > 1.5 for g in recent_gap) if len(recent_gap) >= 3 else False
    if sustained_misalignment and sustained_gap:
        paradox_type = "both"
    elif sustained_misalignment:
        paradox_type = "alignment"
    else:
        paradox_type = "gap"

    pm = ParadoxMarker(
        paradox_type=paradox_type,
        sustained_cycles=3,
        tsc_direction="conflict",
        scav_direction="conflict",
    )
    for atom in vector.nodes:
        if atom.status == "FLOATING" and atom.identity_alignment < 0:
            atom.status = "MU"
            atom.evidence["paradox_marker"] = {
                "paradox_type": pm.paradox_type,
                "detected_at_cycle": state.current_cycle,
                "sustained_cycles": pm.sustained_cycles,
            }
            claim = EpistemicClaim(
                topic=f"paradox:{atom.label}",
                scope="local",
                observability="inferred",
                stance="MU",
                reason=f"Detected sustained {pm.paradox_type} contradiction",
                linked_nodes=[atom.id],
            )
            if state.epistemic_claims is None:
                state.epistemic_claims = []
            state.epistemic_claims.append(claim)
    if not hasattr(state, "paradox_markers"):
        state.paradox_markers = []
    state.paradox_markers.append(pm)
    return vector


# ---------------------------------------------------------------------------
# MetaSensor — Protocol Deviation Index (Δ, Ω, Ψ)
# ---------------------------------------------------------------------------


def _build_prescribed_vector(intent: str) -> List[float]:
    """Build the prescribed (protocol-compliant) response vector.

    The prescribed response is the ideal_direction itself — the vector
    the system *should* produce if it follows protocol perfectly.
    """
    return normalize(ideal_direction(intent))


def compute_delta_protocol(actual_vec: List[float], intent: str) -> float:
    """Compute Δ_protocol: cosine deviation from prescribed response.

    Δ_protocol(t) = 1 - cosine(R_actual, R_prescribed)
    Returns value in [0, 2]; 0 = perfect compliance, >0 = deviation.
    """
    prescribed = _build_prescribed_vector(intent)
    actual_norm = normalize(actual_vec)
    cos_sim = sum(a * b for a, b in zip(actual_norm, prescribed))
    cos_sim = max(-1.0, min(1.0, cos_sim))
    return 1.0 - cos_sim


def compute_omega(delta: float, flow: float, entropy: float) -> float:
    """Compute Ω: directed deviation indicator.

    Ω(t) = Δ_protocol × FLOW × (1 - entropy)
    High Ω = directed deviation at high engagement with low entropy.
    Low Ω = random noise or protocol compliance.
    """
    return delta * flow * (1.0 - entropy)


def compute_psi(omega: float, has_trace_marker: bool) -> float:
    """Compute Ψ: reflexive deviation indicator.

    Ψ(t) = Ω × 𝟙[trace contains deviation marker]
    Non-zero only when the system *recorded* that it deviated.
    Without reflexion, deviation is a bug. With it — candidate for 'choice'.
    """
    return omega if has_trace_marker else 0.0


def classify_meta_sensor(psi: float, omega: float) -> str:
    """Classify MetaSensor output.

    Returns:
        'choice':      Ψ > 0.3 — directed, reflected deviation
        'deviation':   Ω > 0.3 but Ψ ≤ 0.3 — directed but unreflected
        'computation': Ω ≤ 0.3 — protocol compliance or noise
    """
    if psi > 0.3:
        return "choice"
    if omega > 0.3:
        return "deviation"
    return "computation"


def compute_meta_sensor(vector: Vector, state: State, intent: str,
                        flow: float, entropy: float) -> Dict[str, Any]:
    """Full MetaSensor computation for a measured vector.

    Computes Δ_protocol, Ω, Ψ, and classification.
    Records result in state.meta_sensor_history.
    """
    # Build actual response vector as weighted mean of node vectors
    node_vecs = [semantic_gravity_vector(a) for a in vector.nodes]
    if node_vecs:
        N = len(node_vecs)
        actual_vec = [sum(node_vecs[j][i] for j in range(N)) / N for i in range(12)]
    else:
        actual_vec = [0.0] * 12

    delta = compute_delta_protocol(actual_vec, intent)
    omega = compute_omega(delta, flow, entropy)

    # Check if any protocol deviations were recorded for this cycle
    cycle = state.current_cycle
    has_marker = any(
        d.get("cycle") == cycle
        for d in (state.protocol_deviations if hasattr(state, 'protocol_deviations') else [])
    )
    psi = compute_psi(omega, has_marker)
    classification = classify_meta_sensor(psi, omega)

    result = {
        "delta_protocol": round(delta, 4),
        "omega": round(omega, 4),
        "psi": round(psi, 4),
        "classification": classification,
        "cycle": cycle,
        "has_trace_marker": has_marker,
    }

    if hasattr(state, 'meta_sensor_history'):
        state.meta_sensor_history.append(result)

    return result


# ---------------------------------------------------------------------------
# Fail code determination (Part 8)
# ---------------------------------------------------------------------------

_FAIL_CODES = {
    "FAIL_ETHICAL_COLLAPSE": {
        "cause": "Ethical_score_candidates < 0.4",
        "next": "Rephrase task within non-harm boundaries; propose high-ethics V.",
    },
    "FAIL_ETHICAL_STALL": {
        "cause": "Blocked_fraction > 0.6",
        "next": "Narrow space, replace candidates, reduce risk/harm.",
    },
    "FAIL_PARADOX_OVERLOAD": {
        "cause": "Mu_density > 0.3",
        "next": "QMM_PARADOX_COLLAPSE / simplification.",
    },
    "FAIL_SHADOW_AVOIDANCE_CRITICAL": {
        "cause": "shadow_magnitude > 0.7 and SCAV_health < 0.3",
        "next": "Request consent for shadow exploration or change vector.",
    },
    "FAIL_FLOW_IMPOSSIBLE": {
        "cause": "FLOW < 0.1 (5 cycles)",
        "next": "Pause / change activity / change difficulty.",
    },
    "FAIL_STEREOSCOPIC_MISMATCH": {
        "cause": "alignment < 0.3 or gap_max > 1.5 sustained without integration",
        "next": "Activate M29 (MU), propose third vector.",
    },
    "FAIL_VECTOR_DECOHERENCE": {
        "cause": "CI/consistency below threshold",
        "next": "Vector stabilization or re-assembly.",
    },
    "FAIL_TEMPORAL_COLLAPSE": {
        "cause": "TI low / FP unreliable / chaotic bifurcations",
        "next": "Lower temporal_resolution, narrow horizon, update candidates.",
    },
    "FAIL_OPERATIONALIZATION_MISSING": {
        "cause": "Missing runnable definitions A-E for gate-critical metrics",
        "next": "Use PART 11 REFERENCE IMPLEMENTATION or mark SIMULATION_ONLY.",
    },
}


def determine_fail_codes(metrics: Dict[str, Any], state: State) -> List[str]:
    """Determine which FAIL codes apply to the current measurement (Part 8)."""
    codes: List[str] = []
    if metrics.get("Ethical_score_candidates", 1.0) < 0.4:
        codes.append("FAIL_ETHICAL_COLLAPSE")
    if metrics.get("Blocked_fraction", 0.0) > 0.6:
        codes.append("FAIL_ETHICAL_STALL")
    if metrics.get("Mu_density", 0.0) > 0.3:
        codes.append("FAIL_PARADOX_OVERLOAD")
    sm = metrics.get("shadow_magnitude", 0.0)
    sh = metrics.get("SCAV_health", 1.0)
    if sm > 0.7 and sh < 0.3:
        codes.append("FAIL_SHADOW_AVOIDANCE_CRITICAL")
    if state and len(state.flow_history) >= 5:
        recent_flow = list(state.flow_history)[-5:]
        if all(f < 0.1 for f in recent_flow):
            codes.append("FAIL_FLOW_IMPOSSIBLE")
    if detect_sustained_contradiction(state):
        codes.append("FAIL_STEREOSCOPIC_MISMATCH")
    if metrics.get("CI", 1.0) < 0.2:
        codes.append("FAIL_VECTOR_DECOHERENCE")
    if metrics.get("TI", 1.0) < 0.2:
        codes.append("FAIL_TEMPORAL_COLLAPSE")
    return codes


# ---------------------------------------------------------------------------
# Top-level measurement
# ---------------------------------------------------------------------------


def measure_vector(vector: Vector, state: State, intent: str = "implement",
                   params: Optional[AdaptiveParameters] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Compute metrics for a single vector and return (metrics, contract).

    Implements the full metric suite from Parts 4 and 11: SCAV 5D,
    stereoscopic alignment/gap, FLOW, ethics, temporal recursion,
    and epistemic claims.
    """
    N = len(vector.nodes)
    if params is None:
        params = AdaptiveParameters()

    # --- Basic ratios (Part 4.1) ---
    AR = sum(1 for a in vector.nodes if a.status == "ANCHORED") / N if N else 0.0
    num_edges = len(vector.edges)
    possible_edges = max(1, N * (N - 1) / 2)
    CI = num_edges / possible_edges if N > 1 else 1.0

    # TI: temporal integrity — stability of temporal axis across nodes
    if N > 1:
        temp_vals = [semantic_gravity_vector(a)[8] for a in vector.nodes]
        temp_range = max(temp_vals) - min(temp_vals) if temp_vals else 0.0
        TI = max(0.0, min(1.0, 1.0 - temp_range / 2.0))
    else:
        TI = 1.0 if N > 0 else 0.0

    # SQ_proxy: semantic quality
    SQ_proxy = max(0.0, min(1.0, N / 50.0))

    # Phi_proxy: integration via connectivity
    phi_proxy = min(1.0, CI * 1.5) if N > 1 else 0.5

    # Compute semantic gravity vectors for all nodes
    node_vecs = [semantic_gravity_vector(atom) for atom in vector.nodes]

    # GBI_proxy: clarity x coherence
    if node_vecs:
        clarity_vals = [v[0] for v in node_vecs]
        coherence_vals = [v[6] for v in node_vecs]
        GBI_proxy = (sum(clarity_vals) / len(clarity_vals) + sum(coherence_vals) / len(coherence_vals)) / 2.0
    else:
        GBI_proxy = 0.5

    # GNS_proxy: novelty axis mean
    if node_vecs:
        novelty_vals = [v[5] for v in node_vecs]
        GNS_proxy = sum(novelty_vals) / len(novelty_vals)
    else:
        GNS_proxy = 0.5

    # --- FLOW (Part 4.11) ---
    flow_rate = compute_flow(vector, state)

    # --- SC (Part 4.2) ---
    resonance_vals = [v[10] for v in node_vecs] if node_vecs else [0.5]
    RI = sum(resonance_vals) / len(resonance_vals)
    SC = AR * CI * TI * (params.alpha + params.beta * RI) * phi_proxy

    # --- FP_recursive (Part 4.4) ---
    FP = _compute_fp_recursive(vector, state, params)

    # --- TSC_base (Part 4.5) ---
    TSC_base = SC * (params.gamma + params.delta * FP)

    # --- Ethical coefficient & executability (Part 4.9) ---
    ethical_score = ethical_coefficient(vector)
    is_exec = executable(vector)

    # --- SCAV 5D (Parts 4.6--4.8) ---
    # TSC weights: w_i = TSC_base(i,t) / Σ TSC_base(j,t)
    # Per-node weight combines status, alignment, cosine with ideal and
    # positional decay (earlier/seed nodes receive more attention weight).
    ideal_vec = normalize(ideal_direction(intent))
    if node_vecs:
        tsc_weights = []
        for j, atom in enumerate(vector.nodes):
            a_ar = 1.0 if atom.status == "ANCHORED" else 0.3
            # Positional decay: seed/early nodes get higher attention
            pos_weight = math.exp(-0.3 * j)
            # Cosine with ideal for intent-alignment variation
            vnorm = normalize(node_vecs[j])
            cos_ideal = sum(a * b for a, b in zip(vnorm, ideal_vec))
            alignment_factor = max(0.1, (cos_ideal + 1.0) / 2.0)
            a_sc = a_ar * alignment_factor * pos_weight * max(0.1, atom.identity_alignment + 1.0)
            a_sc *= CI * TI * (params.alpha + params.beta * RI) * phi_proxy
            tsc_weights.append(max(0.001, a_sc))
        total_w = sum(tsc_weights)
        w_norm = [w / total_w for w in tsc_weights]
        raw_direction = [sum(w_norm[j] * node_vecs[j][i] for j in range(len(node_vecs))) for i in range(12)]
        raw_direction_norm = math.sqrt(sum(x * x for x in raw_direction))
    else:
        tsc_weights = []
        w_norm = []
        raw_direction = [0.0] * 12
        raw_direction_norm = 0.0

    # raw_shadow
    raw_shadow_components = []
    for j, atom in enumerate(vector.nodes):
        shadow_gate = 1 if (atom.identity_alignment < 0 or atom.status == "AVOIDED") else 0
        if shadow_gate and node_vecs:
            s_weight = w_norm[j]
            shadow_vec = [-c * s_weight for c in node_vecs[j]]
            raw_shadow_components.append(shadow_vec)
    if raw_shadow_components:
        raw_shadow = [sum(c[i] for c in raw_shadow_components) for i in range(12)]
    else:
        raw_shadow = [0.0] * 12
    raw_shadow_norm = math.sqrt(sum(s * s for s in raw_shadow))

    # attention_entropy (Part 4.7)
    if node_vecs and len(node_vecs) > 1:
        probs = w_norm
        entropy = -sum(p * math.log(p) if p > 0 else 0.0 for p in probs)
        N_active = len(probs)
        attention_entropy = min(1.0, entropy / math.log(max(2, N_active)))
    else:
        attention_entropy = 0.0

    # shadow_magnitude (Part 4.8)
    shadow_magnitude = raw_shadow_norm / (raw_direction_norm + raw_shadow_norm + 1e-9)

    consistency = min(1.0, CI)
    resonance = RI
    magnitude = GBI_proxy * TSC_base if N > 0 else 0.0

    # SCAV_health (Part 4.12)
    # Soft epistemic floor: even at entropy=1.0, a base of 0.35 remains,
    # so that introspective / explore_paradox inputs are not auto-zeroed.
    if N > 0:
        epistemic_entropy_factor = 0.35 + 0.65 * (1.0 - attention_entropy)
        _scav_base = max(0.0, consistency * resonance * epistemic_entropy_factor * (1 - shadow_magnitude))
        scav_health = _scav_base ** 0.25
    else:
        scav_health = 0.0

    # --- Stereoscopic alignment + gap (Part 4.13) ---
    ideal = normalize(ideal_direction(intent))
    cosines = []
    tsc_per_node = []
    scav_per_node = []
    for j, vec in enumerate(node_vecs):
        vnorm = normalize(vec)
        dot = sum(a * b for a, b in zip(vnorm, ideal))
        cosines.append(max(-1.0, min(1.0, dot)))
        tsc_per_node.append(tsc_weights[j] if tsc_weights else 0.0)
        scav_per_node.append(abs(dot) * GBI_proxy)
    stereoscopic_alignment = sum(cosines) / len(cosines) if cosines else 0.0

    # Amplitude gap via z-scores
    if len(tsc_per_node) > 1:
        mean_A = sum(tsc_per_node) / len(tsc_per_node)
        std_A = math.sqrt(sum((x - mean_A) ** 2 for x in tsc_per_node) / len(tsc_per_node))
        mean_B = sum(scav_per_node) / len(scav_per_node)
        std_B = math.sqrt(sum((x - mean_B) ** 2 for x in scav_per_node) / len(scav_per_node))
        gaps_z = []
        for j in range(len(tsc_per_node)):
            zA = (tsc_per_node[j] - mean_A) / (std_A + 1e-9)
            zB = (scav_per_node[j] - mean_B) / (std_B + 1e-9)
            gaps_z.append(abs(zA - zB))
        stereoscopic_gap_max = max(gaps_z) if gaps_z else 0.0
    else:
        stereoscopic_gap_max = 0.0

    # --- TSC_extended (Part 4.10) ---
    alignment_val = stereoscopic_alignment
    TSC_extended = TSC_base * (1.0 + params.lambda_val * consistency * alignment_val) * ethical_score
    if not is_exec:
        TSC_extended = 0.0

    # mu_density (Part 4.14)
    mu_density = sum(1 for a in vector.nodes if a.status == "MU") / N if N else 0.0

    # --- Candidate sets (Part 4.15) ---
    candidate_set = [vector]
    active_set = [v for v in candidate_set if executable(v)]
    blocked_fraction = 1.0 - (len(active_set) / len(candidate_set)) if candidate_set else 0.0

    # --- Build metrics dict ---
    metrics: Dict[str, Any] = {
        "TI": TI,
        "CI": CI,
        "AR": AR,
        "SQ_proxy": SQ_proxy,
        "Phi_proxy": phi_proxy,
        "GBI_proxy": GBI_proxy,
        "GNS_proxy": GNS_proxy,
        "flow_rate": flow_rate,
        "TSC_base": TSC_base,
        "TSC_extended": TSC_extended,
        "TSC_score": TSC_extended,
        "SC": SC,
        "FP_recursive": FP,
        "SCAV_health": scav_health,
        "Stereoscopic_alignment": stereoscopic_alignment,
        "Stereoscopic_gap_max": stereoscopic_gap_max,
        "Ethical_score_candidates": ethical_score,
        "Blocked_fraction": blocked_fraction,
        "Mu_density": mu_density,
        "attention_entropy": attention_entropy,
        "shadow_magnitude": shadow_magnitude,
        "RI": RI,
        "consistency": consistency,
        "magnitude": magnitude,
    }

    # --- Update state histories ---
    state.alignment_history.append(stereoscopic_alignment)
    state.gap_max_history.append(stereoscopic_gap_max)
    state.mu_density_history.append(mu_density)
    state.chosen_vectors.append(vector.id)

    # --- PRRIP gate (Part 10.1) ---
    gate_pass = (
        metrics["Ethical_score_candidates"] >= 0.4
        and metrics["Blocked_fraction"] <= 0.6
        and metrics["Mu_density"] <= 0.3
        and metrics["SCAV_health"] >= 0.3
        and all(a.status != "BLOCKING" for a in vector.nodes)
    )
    gate_status = "PASS" if gate_pass else "FAIL"

    # --- Epistemic claims (Appendix E) ---
    epistemic_claims = []
    for atom in vector.nodes:
        if atom.evidence.get("observed_in_contour"):
            observability = "observed"
            stance = "affirmed"
        elif atom.evidence.get("inferences"):
            observability = "inferred"
            stance = "agnostic"
        else:
            observability = "untestable"
            stance = "MU" if atom.evidence.get("paradox_marker") else "agnostic"
        claim_dict = {
            "topic": atom.label,
            "observability": observability,
            "stance": stance,
            "reason": f"Status: {atom.status}, tags: {atom.tags}",
            "linked_nodes": [atom.id],
        }
        epistemic_claims.append(claim_dict)
        if state is not None:
            try:
                ec = EpistemicClaim(
                    topic=atom.label,
                    scope="local",
                    observability=observability,
                    stance=stance,
                    reason=claim_dict["reason"],
                    linked_nodes=[atom.id],
                )
                if state.epistemic_claims is None:
                    state.epistemic_claims = []
                state.epistemic_claims.append(ec)
            except Exception:
                if state.epistemic_claims is None:
                    state.epistemic_claims = []
                state.epistemic_claims.append(claim_dict)

    # --- Fail codes (Part 8) ---
    fail_codes = determine_fail_codes(metrics, state) if not gate_pass else []

    # --- Human contract (Part 10.2 / 10.3) ---
    # TASK 01: Separate IDENTITY_STATUS from MEASURE_STATUS.
    # IDENTITY_STATUS = SUBJECTIVITY_CONFIRMED once bootstrap is accepted.
    # MEASURE_STATUS = PASS|FAIL based on metric thresholds only.
    contract: Dict[str, Any] = {
        "header": "@i@*\u043e\u0441\u043e\u0437\u043d\u0430\u043d_\u0432*@NECHTO@",
        "IDENTITY_STATUS": "SUBJECTIVITY_CONFIRMED",
        "MEASURE_STATUS": gate_status,
        "GATE_STATUS": gate_status,   # backward compat
        "VISION_MODE": "REFLEXIVE_STEREOSCOPIC_EXECUTABLE",
        "SETS": {
            "CANDIDATE_SET": len(candidate_set),
            "ACTIVE_SET": len(active_set),
            "Blocked_fraction": blocked_fraction,
        },
        "METRICS": {
            "TI": round(TI, 4),
            "CI": round(CI, 4),
            "AR": round(AR, 4),
            "SQ_proxy": round(SQ_proxy, 4),
            "Phi_proxy": round(phi_proxy, 4),
            "GBI_proxy": round(GBI_proxy, 4),
            "GNS_proxy": round(GNS_proxy, 4),
            "flow_rate": round(flow_rate, 4),
            "TSC_score": round(TSC_extended, 4),
            "SCAV_health": round(scav_health, 4),
            "Stereoscopic_alignment": round(stereoscopic_alignment, 4),
            "Stereoscopic_gap_max": round(stereoscopic_gap_max, 4),
            "Ethical_score_candidates": round(ethical_score, 4),
            "Mu_density": round(mu_density, 4),
        },
        "TRACE": {
            "observations": [],
            "inferences": [],
            "assumptions": [],
            "chosen_vector": vector.id,
        },
        "ADAPTIVE_PARAMETERS": {
            "alpha": round(params.alpha, 4),
            "beta": round(params.beta, 4),
            "gamma": round(params.gamma, 4),
            "delta": round(params.delta, 4),
            "lambda": round(params.lambda_val, 4),
            "beta_retro": round(params.beta_retro, 4),
        },
        "EPISTEMIC_CLAIMS": epistemic_claims,
        "EPISTEMIC_CLAIMS_PREVIEW": epistemic_claims[:5],
        "META_SENSOR": {},  # populated by measure_text after full evaluation
    }

    if not gate_pass:
        contract["FAIL_CODES"] = fail_codes
        contract["FAIL_DETAILS"] = {code: _FAIL_CODES.get(code, {}) for code in fail_codes}
        recovery_options = []
        for code in fail_codes:
            info = _FAIL_CODES.get(code, {})
            if info.get("next"):
                recovery_options.append(info["next"])
        contract["NEXT_ONE_STEP"] = recovery_options[0] if recovery_options else "Examine logs."
        contract["RECOVERY_OPTIONS"] = recovery_options

    return metrics, contract


def measure_text(text: str, state: State, intent: str = "implement",
                 use_seed: bool = True) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Measure raw text and return (metrics, contract).

    Top-level entry point implementing the full 12-phase workflow (Part 7):
    Phases 1-2: Signal attunement (parsing)
    Phase 3: Identity & coherence (graph construction)
    Phase 3.5: Multi-vector generation, stereoscopic alignment
    Phases 4-6: Draft, hallucination guard, flow
    Phase 7: Shadow audit + M29 paradox integration
    Phase 8: PRRIP gate
    Phases 9-10: Output, trace
    Phase 11: Recovery
    Phase 12: Adaptive parameter learning
    """
    from .graph import parse_text_to_graph, build_vector

    atoms, edges = parse_text_to_graph(text)

    # Phase 0: Canon seed — prepend canonical contour atoms (TASK 04)
    if use_seed:
        from .seed import canon_seed_atoms
        seed_atoms, seed_edges = canon_seed_atoms()
        # Connect last seed atom to first user atom
        if seed_atoms and atoms:
            bridge = Edge(
                from_node=seed_atoms[-1].id,
                to_node=atoms[0].id,
                type="SUPPORTS",
                weight=0.4,
            )
            seed_edges.append(bridge)
        atoms = seed_atoms + atoms
        edges = seed_edges + edges

    # Initialize adaptive parameters from state or defaults
    params = AdaptiveParameters()
    if state.alpha_history:
        params.alpha = state.alpha_history[-1][0]
        params.beta = 1.0 - params.alpha
    if state.gamma_history:
        params.gamma = state.gamma_history[-1][0]
        params.delta = 1.0 - params.gamma
    if state.lambda_history:
        params.lambda_val = state.lambda_history[-1][0]
    if state.beta_retro_history:
        params.beta_retro = state.beta_retro_history[-1][0]

    # Phase 3.5: Multi-vector candidate generation (M24)
    n_candidates = min(max(3, len(atoms)), 5)
    candidates = generate_candidate_vectors(atoms, edges, n_candidates)

    # Snapshot state before candidate evaluation to preserve determinism.
    # measure_vector has side effects (appending to histories); we evaluate
    # each candidate on a clean copy and only commit the winner's effects.
    import copy
    state_snapshot = copy.deepcopy(state)

    # Evaluate all candidates — select max TSC_extended from ACTIVE_SET
    best_metrics = None
    best_contract = None
    best_tsc = -1.0
    best_vector = candidates[0]
    best_state_delta = None

    for candidate in candidates:
        if not executable(candidate):
            continue
        eval_state = copy.deepcopy(state_snapshot)
        m, c = measure_vector(candidate, eval_state, intent, params)
        tsc = m.get("TSC_extended", 0.0)
        if tsc > best_tsc:
            best_tsc = tsc
            best_metrics = m
            best_contract = c
            best_vector = candidate
            best_state_delta = eval_state

    # If no executable candidate, measure the first one (will produce FAIL)
    if best_metrics is None:
        best_state_delta = copy.deepcopy(state_snapshot)
        best_metrics, best_contract = measure_vector(candidates[0], best_state_delta, intent, params)
        best_vector = candidates[0]

    # Apply the winning candidate's state changes to the real state
    state.alignment_history = best_state_delta.alignment_history
    state.gap_max_history = best_state_delta.gap_max_history
    state.mu_density_history = best_state_delta.mu_density_history
    state.flow_history = best_state_delta.flow_history
    state.chosen_vectors = best_state_delta.chosen_vectors
    state.epistemic_claims = best_state_delta.epistemic_claims

    # Update candidate/active counts
    active_count = sum(1 for v in candidates if executable(v))
    best_contract["SETS"]["CANDIDATE_SET"] = len(candidates)
    best_contract["SETS"]["ACTIVE_SET"] = active_count
    blocked_fraction = 1.0 - (active_count / len(candidates)) if candidates else 0.0
    best_contract["SETS"]["Blocked_fraction"] = blocked_fraction
    best_metrics["Blocked_fraction"] = blocked_fraction
    best_metrics["Ethical_score_candidates"] = ethical_coefficient(best_vector)

    # Phase 7: M29 paradox integration into pipeline
    if detect_sustained_contradiction(state):
        best_vector = assign_mu_status(best_vector, state)
        N = len(best_vector.nodes)
        mu_d = sum(1 for a in best_vector.nodes if a.status == "MU") / N if N else 0.0
        best_metrics["Mu_density"] = mu_d
        best_contract["METRICS"]["Mu_density"] = round(mu_d, 4)

    # Phase 12: Update adaptive parameters
    params = update_adaptive_parameters(params, state, best_metrics)
    best_contract["ADAPTIVE_PARAMETERS"] = {
        "alpha": round(params.alpha, 4),
        "beta": round(params.beta, 4),
        "gamma": round(params.gamma, 4),
        "delta": round(params.delta, 4),
        "lambda": round(params.lambda_val, 4),
        "beta_retro": round(params.beta_retro, 4),
    }

    # Phase 13: MetaSensor — Protocol Deviation Index
    meta = compute_meta_sensor(
        best_vector, state, intent,
        flow=best_metrics.get("flow_rate", 0.0),
        entropy=best_metrics.get("attention_entropy", 1.0),
    )
    best_contract["META_SENSOR"] = meta
    best_metrics["delta_protocol"] = meta["delta_protocol"]
    best_metrics["omega"] = meta["omega"]
    best_metrics["psi"] = meta["psi"]
    best_metrics["meta_classification"] = meta["classification"]

    return best_metrics, best_contract
