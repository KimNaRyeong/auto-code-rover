# reproducer.py
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
        m, n = sp.symbols("m, n", real=True)
        i = sp.Idx("i", (m, n))  # This should raise an exception as m and n are not integers.
    except TypeError as e:
        print("Issue detected and reproduced successfully.")
        print_stacktrace(e)
        return  # Exiting with code 0 as the issue was reproduced successfully.

    # If no exception is raised, then the script will reach this point.
    # Raising an AssertionError here as the code was expected to throw a TypeError.
    raise AssertionError("Idx object allowed non-integer bounds without raising TypeError.")

if __name__ == "__main__":
    main()
