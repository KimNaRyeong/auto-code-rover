from sympy import totient
import sys
import traceback

def print_stacktrace(e: Exception):
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
        totient(2.3)
    except Exception as e:
        print_stacktrace(e)
        assert False, "The totient function should raise a TypeError for non-integer numbers"
    else:
        print("The totient function did not raise a TypeError for non-integer numbers")
        assert False, "The issue is not present"

if __name__ == "__main__":
    main()
    # The script should exit with code 0 when the issue is fixed
    exit(0)
