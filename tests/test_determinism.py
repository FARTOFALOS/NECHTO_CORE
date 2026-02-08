from nechto_runtime.metrics import measure_text
from nechto_runtime.types import State


def test_determinism():
    """measure_text should be deterministic for the same input."""
    prompt = "Hello, this is a test prompt."
    state1 = State()
    metrics1, contract1 = measure_text(prompt, state1)
    # Run again with a fresh state
    state2 = State()
    metrics2, contract2 = measure_text(prompt, state2)
    assert metrics1 == metrics2
    assert contract1 == contract2
