"""
reproducer.py

This script is designed to reproduce a specific issue with pylint removing
the first item from sys.path when running from runpy.
"""

import os
import sys
import runpy
from contextlib import redirect_stderr
from io import StringIO


def print_stacktrace(e: Exception):
    """
    Prints the stack trace of the given exception.
    """
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def reproduce_issue():
    """
    Attempts to reproduce the issue with pylint and sys.path.
    """
    # Insert a unique dummy path to sys.path
    dummy_path = "/unique/dummy/path"
    sys.path.insert(0, dummy_path)
    
    # Capture original sys.path for later assertion
    original_sys_path = sys.path[:]

    # Redirect stderr to capture pylint's output for later review
    captured_stderr = StringIO()
    with redirect_stderr(captured_stderr):
        try:
            # Programmatically run pylint as a module
            runpy.run_module('pylint', run_name="__main__", alter_sys=True)
        except Exception as e:
            # pylint is expected to fail due to no args, but we want to inspect sys.path
            print_stacktrace(e)
    
    # Assert the first item of sys.path wasn't incorrectly removed
    if sys.path[0] == dummy_path:
        print("The issue seems to be fixed!")
    else:
        if not sys.path:  # If sys.path is empty, it was completely cleared
            raise AssertionError("sys.path was unexpectedly cleared.")
        elif sys.path[0] in ["", ".", os.getcwd()]:
            raise AssertionError("The first item of sys.path was modified but not as expected.")
        else:
            raise AssertionError("The first item of sys.path was unexpectedly removed.")


if __name__ == "__main__":
    reproduce_issue()
