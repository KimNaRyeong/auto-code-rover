# reproducer.py
from sympy import S

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
    try:
        # The issue demonstrates inconsistency in comparison outcomes based
        # on the order of comparison between S.false and S(0.0)
        assert S(0.0) == S.false, "S(0.0) == S.false should return True, but it doesn't."
        assert S.false == S(0.0), "S.false == S(0.0) should return True, but it doesn't."
        print("No issue, both assertions passed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # exit with non-zero status to indicate failure

if __name__ == "__main__":
    main()
