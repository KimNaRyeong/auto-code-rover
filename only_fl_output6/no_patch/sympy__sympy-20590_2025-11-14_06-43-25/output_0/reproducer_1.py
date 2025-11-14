import sympy
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

def check_symbol_dict():
    try:
        # Attempt to access __dict__ of a sympy.Symbol instance
        _ = sympy.Symbol('x').__dict__
        # If no AttributeError, it means __dict__ exists, which is not expected before sympy 1.7
        has_dict_issue = True
    except AttributeError:
        # If AttributeError is raised, it means __dict__ does not exist, which is expected
        has_dict_issue = False

    try:
        assert not has_dict_issue, "Symbol instances should not have a __dict__ attribute."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Issue is present, exit with error code

    # If the execution reaches here, it means __dict__ does not exist as expected, or the issue is fixed
    print("No issue detected, exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    check_symbol_dict()
