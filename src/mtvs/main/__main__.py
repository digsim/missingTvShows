import sys

from .mainImpl import MainImpl


def cli() -> None:
    """Entry point for the application script defined in pyproject.toml"""
    main = MainImpl()
    main.get_arguments(sys.argv[1:])


if __name__ == "__main__":
    cli()
