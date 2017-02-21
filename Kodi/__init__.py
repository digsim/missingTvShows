from __future__ import unicode_literals
import sys
from .missing_tvshows import TVShows

def main():
    """Entry point for the application script"""
    sms = TVShows()
    sms.getArguments(sys.argv[1:])