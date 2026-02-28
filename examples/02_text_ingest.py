from nechto import NechtoEngine


if __name__ == "__main__":
    result = NechtoEngine().process_text("build a small plan")
    print(getattr(result, "gate_status", "UNKNOWN"))
