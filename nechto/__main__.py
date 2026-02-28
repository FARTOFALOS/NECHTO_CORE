"""Allow running NECHTO as `python -m nechto`."""

from nechto.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
