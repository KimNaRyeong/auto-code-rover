# reproducer.py
import sympy as sp

def check_evalf_on_quaternion():
    try:
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        result = q.evalf()  # Expected to produce a numerical result
        # Checking if the result is evaluated correctly
        assert result != q, "Quaternion evalf() did not return a numerical result."
        print("Success: Quaternion evalf method works as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero value to indicate failure

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
    check_evalf_on_quaternion()
