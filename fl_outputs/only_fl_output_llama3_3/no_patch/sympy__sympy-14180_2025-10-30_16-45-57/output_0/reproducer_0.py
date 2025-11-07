import math
from typing import Any

def print_stacktrace(e: Exception) -> None:
    """Prints the stack trace of an exception."""
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

def reproduce_issue() -> None:
    try:
        latex_expression = "ln(10)"
        converted_expression = f"latex({latex_expression})"
        assert converted_expression == r"\ln\left(10\right)", f"Issue: {converted_expression} != \ln\left(10\right)"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue fixed, exiting with code 0")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
