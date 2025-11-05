import sys
import importlib.util
from unittest.mock import patch
import os

def main():
    if len(sys.argv) != 2 or sys.argv[1] != 'runserver':
        raise AssertionError("Expected -m custom_module runserver, but got {}".format(' '.join(sys.argv)))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

