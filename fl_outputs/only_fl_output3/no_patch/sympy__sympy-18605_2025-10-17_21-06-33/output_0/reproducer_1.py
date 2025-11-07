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

def test_idx_with_non_integer_bounds():
    m, n = sp.symbols("m, n", real=True)
    try:
        i = sp.Idx("i", (m, n))  # This should not work according to the issue description
        print("Test passed: Idx constructor did not raise an exception for non-integer bounds.")
    except Exception as e:
        print_stacktrace(e)
        assert "Idx object requires an integer dimension." in str(e), "The message is not as expected."

if __name__ == "__main__":
    m, n = sp.symbols("m, n", real=True)
    # Directly test without the try-except to let any exceptions raise naturally if the issue persists
    i = sp.Idx("i", (m, n))  # This is the critical test case
    try:
        # If the script reaches this point without errors, there's an issue
        raise AssertionError("Idx object accepted non-integer bounds without raising an error.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with an error code to indicate the presence of the issue
    except Exception as e:
        # Catch and print any unexpected exceptions
        print_stacktrace(e)
        exit(1)  # Exit with an error code to indicate a problem occurred

    # If no exceptions are raised, the issue is not present, exit with code 0
    print("Test succeeded: Idx object behaved as expected with integer bounds.")
    exit(0)
