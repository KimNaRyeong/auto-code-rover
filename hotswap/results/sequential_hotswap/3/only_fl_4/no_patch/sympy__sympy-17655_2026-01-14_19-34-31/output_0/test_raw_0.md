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

def test_operation():
    from sympy import geometry as ge
    import sympy

    point1 = ge.Point(0,0)
    point2 = ge.Point(1,1)

    # This line works fine
    result1 = point1 + point2 * sympy.sympify(2.0)

    try:
        # Attempt the operation that is expected to raise an exception
        result2 = point1 + sympy.sympify(2.0) * point2
        assert result1 == result2, "The results differ, which is unexpected."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected exception occurred.")

if __name__ == "__main__":
    test_operation()
```