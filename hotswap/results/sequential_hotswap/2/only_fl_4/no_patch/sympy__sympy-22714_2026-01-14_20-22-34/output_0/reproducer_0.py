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

def reproducer():
    import sympy as sp
    try:
        with sp.evaluate(False):
            sp.S('Point2D(Integer(1),Integer(2))')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

    try:
        sp.S('Point2D(Integer(1),Integer(2))')
        sp.S('Point2D(Integer(1),Integer(2))', evaluate=False)
        return 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpectedly failed outside the context manager.")

if __name__ == "__main__":
    reproducer()
