from sympy import symbols, ask, Q
from sympy.abc import x, y, z

def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    p = symbols('p', real=True, zero=False)
    q = symbols('q', zero=True)
    result = (q**p).is_positive
    expected_result = False
    assert result == expected_result, f"Expected {expected_result} but got {result}"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
