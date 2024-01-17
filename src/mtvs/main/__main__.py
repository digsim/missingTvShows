# -*- coding: utf-8 -*-
import sys
from .mainImpl import MainImpl


def cli():
    """Entry point for the application script defined in pyproject.toml"""
    main = MainImpl()
    main.getArguments(sys.argv[1:])


if __name__ == "__main__":
    cli()
