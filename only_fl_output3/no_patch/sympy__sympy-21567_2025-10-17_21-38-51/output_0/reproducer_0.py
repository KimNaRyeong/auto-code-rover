# reproducer.py
from sympy import symbols, expand_trig, tanh, csch, sech, csc, sin, cos
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

def test_expand_trig():
    x, y = symbols('x y')
    # Test cases for tanh, csch, sech to reproduce the issue
    try:
        # For tanh, check if the output matches the expected expanded form
        assert expand_trig(tanh(x + y)) == (tanh(x) + tanh(y))/(tanh(x)*tanh(y) + 1), "tanh expansion failed"

        # For csch, check if it expands similarly to how csc does
        assert expand_trig(csch(x + y)) != csch(x + y), "csch expansion failed"

        # For sech, check if it expands similarly to how sec does
        assert expand_trig(sech(x + y)) != sech(x + y), "sech expansion failed"

        # Passes if all expansion checks are successful
        print("All expansions successful. Issue may be resolved.")
        
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status when assertion fails

if __name__ == "__main__":
    test_expand_trig()
    sys.exit(0)
