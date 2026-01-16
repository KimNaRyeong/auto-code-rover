# reproducer.py
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

def main():
    from sympy import sympify

    try:
        expr = sympify("cosh(acos(-i + acosh(-g + i)))")
        # is_zero may not strictly raise an exception; it can just return None or False
        # But in this case, if there is a maximum recursion depth issue, it would already have raised
        is_zero_result = expr.is_zero
        assert is_zero_result is not True, "Expected not True for is_zero but got True"
        # Since the operation leads to RecursionError we assert for its absence indicating the bug is fixed
    except RecursionError as e:
        print_stacktrace(e)
        assert False, "RecursionError encountered, issue is present"
    except AssertionError as e:
        raise e
    except Exception as e:
        print_stacktrace(e)
        assert False, f"An unexpected error occurred: {e}"
    else:
        print("No RecursionError, issue appears to be fixed or not present")

if __name__ == "__main__":
    sys.exit(main())
