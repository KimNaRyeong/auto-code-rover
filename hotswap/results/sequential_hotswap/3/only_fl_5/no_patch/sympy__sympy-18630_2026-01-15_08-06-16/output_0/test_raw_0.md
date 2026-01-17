```python
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
    from sympy import integrate, Symbol, S, oo
    x = Symbol('x')
    try:
        # Attempt to perform an integration that is expected to cause an error.
        integrate(1 / (1 + x**4)**(S(1)/4), [x, 0, oo])
        # If the integration does not raise an error, we assert to ensure the reproducibility test fails.
        assert False, "Issue did not occur."
    except AttributeError as e:
        # Check if the exception is exactly what we expect.
        # This string check is fragile since it depends on the specific error message, consider removing it
        # for a broader catch if the specifics of the message are not critical.
        assert str(e) == "'TupleArg' object has no attribute 'compute_leading_term'", "Unexpected error message."
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        # If an AssertionError occurs, we print it and exit with code 1.
        # This includes failing the assertion in the try block above if the issue was not encountered.
        print(e)
        exit(1)
    # If the script did not exit by this point, it means the issue was successfully reproduced.
    # You may choose to explicitly exit with code 0 to denote success, but it's not strictly necessary as the
    # script will exit with code 0 by default if it reaches the end without errors.
    print("Issue successfully reproduced.")
```

This script aims to precisely fulfill the conditions you described: it reproduces the issue, asserting its occurrence, and prints detailed information about the exception when it happens. Exiting with code 1 on assertion failure and printing the stack trace of the AttributeError exception help identify whether the issue is present or not clearly.