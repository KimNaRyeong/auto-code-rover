```python
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
    from sympy import MatrixSymbol, latex
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)

    # Define an AssertionError for each type of printer if the output is not as expected.
    try:
        assert str(A - A*B - B) == "A - A*B - B", "str printer matrix subtraction failed"
    except AssertionError as e:
        print_stacktrace(e)

    try:
        # Using pretty print as a regular string for assertions since pprint directly prints to sys.stdout.
        from sympy import pretty
        assert pretty(A - A*B - B) == "A - A*B - B", "pretty printer matrix subtraction failed"
    except AssertionError as e:
        print_stacktrace(e)

    try:
        assert latex(A - A*B - B) == "A - A B - B", "latex printer matrix subtraction failed"
    except AssertionError as e:
        print_stacktrace(e)

# Ensure main only runs when this script is executed directly
if __name__ == "__main__":
    main()
    print("Script finished. If no AssertionError was raised, the issue is fixed.")
```

This script verifies the functionality of symbolically subtracting `MatrixSymbol` objects and printing them using different SymPy printers (`str`, `pretty`, and `latex`). For each printer, it checks whether the output matches the expected string format for matrix subtraction (e.g., "A - A*B - B"). If the outputs do not match the expected format, it raises an `AssertionError` and prints a detailed stack trace for debugging purposes. If no errors are raised, it indicates that the issue has been resolved.