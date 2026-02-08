from nechto_runtime.graph import parse_graph
from nechto_runtime.metrics import ged_proxy_norm


def test_ged_proxy_norm_identical():
    """ged_proxy_norm should be 0 for identical graphs"""
    g1 = parse_graph("A:1\nB:2")
    g2 = parse_graph("A:1\nB:2")
    assert ged_proxy_norm(g1, g2) == 0.0


def test_ged_proxy_norm_different():
    """ged_proxy_norm should be >0 for different graphs"""
    g1 = parse_graph("A:1\nB:2")
    g2 = parse_graph("A:1\nB:2\nC:3")
    assert ged_proxy_norm(g1, g2) > 0.0
