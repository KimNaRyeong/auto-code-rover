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
        str(sp.OneMatrix(2, 2))
        str(sp.ZeroMatrix(2, 2))
        str(sp.Identity(3, 3))  # Changed the size of Identity matrix
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
