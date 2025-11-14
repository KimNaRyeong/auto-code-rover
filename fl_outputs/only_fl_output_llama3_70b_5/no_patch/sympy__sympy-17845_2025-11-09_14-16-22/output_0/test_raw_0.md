Here is the `reproducer.py` file that reproduces the issue:
```
from sympy import Interval, FiniteSet

def print_stacktrace(e: Exception):
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

def test_interval():
    interval_str = str(Interval(0,1))
    expected_str = "Interval(0, 1)"
    try:
        assert interval_str == expected_str
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

def test_finiteset():
    finite_set_str = str(FiniteSet(1,2,3))
    expected_str = "FiniteSet(1, 2, 3)"
    try:
        assert finite_set_str == expected_str
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_interval()
    test_finiteset()
```
<|start_header_id|>