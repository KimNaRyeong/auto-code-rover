import sys
import traceback
from sympy import pprint, DiracDelta, symbols
from sympy.abc import x

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        pprint(x*DiracDelta(x, 1))
    except TypeError as e:
        print_stacktrace(e)
        assert False, "TypeError raised"
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected exception raised"
    else:
        assert False, "No exception raised"

sys.exit(0)
