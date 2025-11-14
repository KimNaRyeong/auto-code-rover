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

def main():
    from sympy import geometry as ge
    import sympy

    try:
        point1 = ge.Point(0, 0)
        point2 = ge.Point(1, 1)
        point1 + sympy.sympify(2.0) * point2
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected both lines to work without raising an exception")

if __name__ == "__main__":
    main()
