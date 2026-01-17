```python
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

def test_sympy_behavior():
    import sympy as sy
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)
    result1 = sy.Matrix.hstack(M1, M2, M3, M4).shape

    M5 = sy.Matrix.zeros(1, 0)
    M6 = sy.Matrix.zeros(1, 1)
    M7 = sy.Matrix.zeros(1, 2)
    M8 = sy.Matrix.zeros(1, 3)
    result2 = sy.Matrix.hstack(M5, M6, M7, M8).shape

    try:
        assert result1 == (0, 6), f"Incorrect result1 shape {result1}, expected (0, 6)"
        assert result2 == (1, 6), f"Incorrect result2 shape {result2}, expected (1, 6)"
        return 0
    except AssertionError as e:
        print_stacktrace(e)
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(test_sympy_behavior())
```