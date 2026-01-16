# reproducer.py
from sympy import sqrt, I, simplify
from sympy.core.compatibility import exec_

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
        # The expression that was causing issues
        expr = sqrt((3 + 4*I)/(3 - 4*I))
        # Calculating the simplified form of the expression to compare
        simplified_expr = simplify(expr)
        # Incorrect result based on the issue description
        incorrect_result = sqrt(-1/(3 - 4*I))*sqrt(-3 - 4*I)

        # Check if the issue is still present by comparing the simplified expression to the incorrect result
        if simplify(simplified_expr - incorrect_result) == 0:
            raise AssertionError("sqrt splits out non-real factors incorrectly.")

    except AssertionError as e:
        print("Issue detected:")
        print_stacktrace(e)
        # Exiting with a non-zero exit code to indicate the presence of the issue
        exit(1)
    except Exception as e:
        print("An error occurred:")
        print_stacktrace(e)
        # Exiting with a non-zero exit code in case of unexpected errors
        exit(1)
    else:
        print("No issue detected, the expression is handled correctly.")
        # Exiting with code 0 when the issue is fixed or not detected
        exit(0)

if __name__ == "__main__":
    main()
