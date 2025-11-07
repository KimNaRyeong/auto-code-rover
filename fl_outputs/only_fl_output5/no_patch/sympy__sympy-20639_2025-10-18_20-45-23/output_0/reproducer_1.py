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

def reproduce_issue():
    from sympy import symbols, pi, E, latex, exp, pretty

    # Reproducing the issue with pretty printing
    expr = pi**(1/E)
    
    # Generating the pretty print output
    pretty_output = pretty(expr)

    # Attempting to identify the issue articulated in the problem statement
    # i.e., verifying if the pretty print representation is -1___╲╱ π 
    unexpected_pretty_output = "-1___\n╲╱ π "
    try:
        assert pretty_output != unexpected_pretty_output, "Unexpected pretty print representation detected."
    except AssertionError as e:
        print("Detected the reported issue with pretty printing of pi**(1/E).")
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        reproduce_issue()
        # If the assertion does not fail, it means the unexpected pretty print was not produced
        print("The issue with pretty printing pi**(1/E) was not detected.")
        exit(0)
    except AssertionError:
        # Exiting with a non-zero code to indicate the reproduction of the issue
        exit(1)
