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

try:
    # Importing sympy library
    import sympy as sp

    # Defining the expression that causes the issue
    function = sp.Pow(sp.LambertW(2), 2)

    # Trigger display to simulate JupyterLab's display mechanism
    display_str = sp.printing.latex(function)
    
    # If exception not raised part
    print("Issue resolved. Exiting with code 0.")
    exit(0)

except Exception as e:
    # Print the stacktrace if the exception occurs.
    print_stacktrace(e)
    raise AssertionError("The issue is present.")
