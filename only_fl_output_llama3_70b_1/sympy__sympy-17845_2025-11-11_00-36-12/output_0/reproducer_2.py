from sympy import Interval, FiniteSet

def test_principle():
    interval_str = str(Interval(0, 1))
    finite_set_str = str(FiniteSet(1, 2, 3))

    assert interval_str == "Interval(0, 1, False, False)"
    assert finite_set_str == "{1, 2, 3}"

def main():
    try:
        test_principle()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    main()
