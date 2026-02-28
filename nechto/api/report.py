def report_metrics(result) -> dict:
    return getattr(result, "metrics", {}) or {}
