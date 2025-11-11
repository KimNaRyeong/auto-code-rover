import pylint.lint as lint
import sys

def print_stacktrace(e: Exception):
    import traceback    
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    code = """
\"\"\"Docstring.\"\"\

import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
"""

    with open("a.py", "w") as f:
        f.write(code)

    try:
        lint.Run(["a.py"])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("unused-import false positive for a module used in a type comment")
        else:
            print("Issue is fixed")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
