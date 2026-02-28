from nechto.engine import NechtoEngine


def run(raw_input: str = "", context: dict | None = None):
    return NechtoEngine().run(raw_input, context=context)
