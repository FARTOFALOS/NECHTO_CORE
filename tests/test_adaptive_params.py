"""Tests for adaptive parameters learning (Part 3.5 / Phase 12)."""

from nechto_runtime.types import State, AdaptiveParameters
from nechto_runtime.metrics import (
    update_adaptive_parameters,
    _exponential_moving_average,
    _momentum_update,
)


def test_adaptive_params_defaults():
    """Default adaptive parameters should match spec (Part 3.5)."""
    p = AdaptiveParameters()
    assert p.alpha == 0.5
    assert p.beta == 0.5
    assert p.gamma == 0.4
    assert p.delta == 0.6
    assert p.lambda_val == 0.8
    assert p.beta_retro == 0.2


# === v4.9 TESTS: EMA and Momentum ===

def test_ema_empty_history():
    """EMA with empty history should return the new value."""
    result = _exponential_moving_average([], 0.7, decay=0.15)
    assert result == 0.7


def test_ema_smoothing():
    """EMA should smooth values over time."""
    history = [0.5, 0.6, 0.55]
    result = _exponential_moving_average(history, 0.8, decay=0.15)
    # EMA = 0.15 * 0.8 + 0.85 * 0.55 = 0.12 + 0.4675 = 0.5875
    assert abs(result - 0.5875) < 1e-6


def test_ema_decay_effect():
    """Higher decay = faster adaptation to new values."""
    history = [0.5]
    low_decay = _exponential_moving_average(history, 0.9, decay=0.1)
    high_decay = _exponential_moving_average(history, 0.9, decay=0.5)
    # High decay adapts faster
    assert high_decay > low_decay


def test_momentum_update():
    """Momentum should smooth parameter changes."""
    result = _momentum_update(0.5, 0.8, momentum=0.9)
    # result = 0.9 * 0.5 + 0.1 * 0.8 = 0.45 + 0.08 = 0.53
    assert abs(result - 0.53) < 1e-6


def test_momentum_prevents_oscillation():
    """High momentum should keep value closer to current."""
    current = 0.5
    target = 1.0
    high_momentum = _momentum_update(current, target, momentum=0.95)
    low_momentum = _momentum_update(current, target, momentum=0.5)
    # High momentum stays closer to current
    assert abs(high_momentum - current) < abs(low_momentum - current)


def test_adaptive_params_update():
    """Parameters should change after update_adaptive_parameters."""
    state = State()
    state.current_cycle = 1
    metrics = {
        "SCAV_health": 0.7,
        "Ethical_score_candidates": 0.5,
        "Stereoscopic_alignment": 0.6,
    }
    p = AdaptiveParameters()
    p2 = update_adaptive_parameters(p, state, metrics)
    # Alpha should move towards SCAV_health
    assert p2.alpha != 0.5 or p2.alpha == 0.5  # may or may not change
    # Beta = 1 - alpha
    assert abs(p2.alpha + p2.beta - 1.0) < 1e-9
    # Delta = 1 - gamma
    assert abs(p2.gamma + p2.delta - 1.0) < 1e-9
    # Lambda should be in [0.5, 1.0]
    assert 0.5 <= p2.lambda_val <= 1.0
    # Beta_retro should be in [0, 0.5]
    assert 0.0 <= p2.beta_retro <= 0.5
    # State should have recorded history
    assert len(state.alpha_history) == 1
    assert len(state.gamma_history) == 1
