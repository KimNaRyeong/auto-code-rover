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
    from sympy import Symbol, S, SympifyError

    try:
        # Attempt to create a symbolic variable with a greek letter using sympify
        alpha_symbol = S("α")
        print(f"Successfully sympified: {alpha_symbol}")
        # Assuming the expected output includes the alpha symbol without errors
    except SympifyError as e:
        print_stacktrace(e)
        print("SympifyError encountered as expected due to the issue being present.")
        raise AssertionError("SympifyError occurred: the issue is still present.")
    except Exception as e:
        # Catching any other unexpected errors and printing their stack traces
        print_stacktrace(e)
        raise AssertionError(f"An unexpected error occurred: {e}")
    else:
        print("No issues detected. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    main()
