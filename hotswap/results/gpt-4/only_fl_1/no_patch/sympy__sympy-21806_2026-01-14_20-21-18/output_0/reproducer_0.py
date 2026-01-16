# reproducer.py

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
    import sympy as sp
    try:
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        evalf_q = q.evalf()  # Attempt to call evalf on a Quaternion instance
        # Checking if evalf works improperly by still showing sqrt terms without numerical evaluation
        assert str(evalf_q) != "sqrt(2)/2 + 0*i + 0*j + sqrt(2)/2*k", "Quaternion evalf() might not be working properly."
    except AssertionError as e:
        # Print stacktrace and propagate the assertion error if the assertion fails
        print_stacktrace(e)
        raise
    except Exception as e:
        # For any other exception, print the stacktrace but do not re-raise it to simulate a "soft" error catch
        print_stacktrace(e)
        print("An unexpected error occurred, indicating a potential issue with Quaternion evalf() method.", file=sys.stderr)
    else:
        print("No issue detected. Quaternion evalf() method seems to be working as expected.")

if __name__ == "__main__":
    main()
