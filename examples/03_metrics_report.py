from nechto import NechtoEngine


if __name__ == "__main__":
    result = NechtoEngine().run("implement", context={"intent": "implement"})
    print(getattr(result, "metrics", {}))
