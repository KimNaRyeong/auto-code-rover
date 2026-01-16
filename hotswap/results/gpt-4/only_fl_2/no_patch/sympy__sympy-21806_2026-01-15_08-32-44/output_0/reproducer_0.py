import sympy as sp

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
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        evaluated = q.evalf()
        # Verify if evalf method works as expected
        # This condition checks if the issue is present.
        # When the evalf method works as expected, the output will be a
        # numerical approximation and not an expression with sqrt.
        if isinstance(evaluated, sp.Quaternion) and all(isinstance(val, sp.Float) for val in evaluated.args):
            print("evalf method works correctly for Quaternion.")
        else:
            raise AssertionError("Quaternion evalf method does not evaluate to numerical approximations.")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
