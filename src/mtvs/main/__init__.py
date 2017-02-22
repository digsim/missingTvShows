# -*- coding: utf-8 -*-
import sys
from .mainImpl import MainImpl


def main():
    """Entry point for the application script defined in setup.py"""
    main = MainImpl()
    main.getArguments(sys.argv[1:])
