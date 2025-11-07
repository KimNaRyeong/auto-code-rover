```python
# reproducer.py
from sympy.solvers.diophantine import diophantine
from sympy import symbols

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

def test_diophantine_inconsistency():
    m, n = symbols('m n')
    result_1 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m, n), permute=True)
    result_2 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n, m), permute=True)
    # Check if both results match, if not raise AssertionError
    assert result_1 == result_2, "diophantine produces inconsistent results based on symbols order"

if __name__ == "__main__":
    try:
        test_diophantine_inconsistency()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    print("No issues found.")
    raise SystemExit(0)
```