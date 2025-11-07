Certainly! Below is the `reproducer.py` file. It uses SymPy to compute the degree of a rational function and checks if the behavior matches the expectation. If SymPy's behavior deviates from what's expected, it raises an `AssertionError` which triggers the stack trace to be printed.

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

def test_degree_of_rational_function():
    from sympy import symbols, degree

    # Define the variable
    x = symbols('x')

    # Define the rational function
    rational_function = (x-2)/(x**2+1)

    try:
        # Compute the degree of the rational function
        result = degree(rational_function, x)

        # Check if the result matches the expectation
        assert result != 1, "Degree computation of rational functions is not behaving as expected."
        print("The issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_degree_of_rational_function()
```

This script starts by defining a function `test_degree_of_rational_function` which computes the degree of a given rational function \((x-2)/(x^2+1)\) using SymPy. The script expects SymPy to handle the degree computation of rational functions correctly. However, based on your description, SymPy returns 1 as the degree, which suggests that SymPy's behavior may not align with the expected handling of rational functions. The assertion checks if the computed result deviates from this unexpected result (i.e., `result != 1`). If the behavior is indeed incorrect and results in an unexpected value (in this case, `1`), it raises an `AssertionError`, triggering the `print_stacktrace` function to output a detailed stack trace.

Make sure you have SymPy installed in your environment before running the script. You can do so using pip:
```
pip install sympy
```