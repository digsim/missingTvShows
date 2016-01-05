from __future__ import unicode_literals
import sys
import signal
from missing_tvshows import TVShows



def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    real_raw_input = vars(__builtins__).get('raw_input',input)

    try:
        if real_raw_input('\nReally quit? (y/n)> ').lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)

original_sigint = signal.getsignal(signal.SIGINT)

def main():
    """Entry point for the application script"""
    signal.signal(signal.SIGINT, exit_gracefully)
    sms = TVShows()
    sms.getArguments(sys.argv[1:])