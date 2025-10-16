Based on your requirements for a reproducible test scenario, the script below `reproducer.py` is crafted to check the specified eigenvalue computation issue with SymPy and outputs appropriately, including raising an `AssertionError` when the expected outcome from `.eigenvals()` is not achieved. It also integrates the function to correctly print the traceback for any exceptions encountered.

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

def test_eigenvalues_computation():
    from sympy import symbols, Matrix, eye, exp, solve

    # Define the symbolic variable x
    x = symbols('x')
    # Define the matrix M
    M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])

    try:
        # Attempt to find the eigenvalues using the eigenvals() method
        eigenvals_result = M.eigenvals()
        # Check to ensure that the result is not empty
        assert eigenvals_result, "Eigenvalues computation using .eigenvals() failed."
    except Exception as e:
        print_stacktrace(e)
        try:
            # If .eigenvals() failed, try solving directly using characteristic polynomial
            lam = symbols('lambda')
            roots_result = solve((M - lam * eye(3)).det(), lam)
            # This assertion fails if roots_result is empty, implying .eigenvals() should have worked
            assert roots_result, "Failed to compute eigenvalues directly through characteristic polynomial."
            print("Successfully computed eigenvalues directly, suggesting an issue with .eigenvals().")
            exit(1)
        except Exception as inner_exc:
            print_stacktrace(inner_exc)
            raise AssertionError("Both .eigenvals() and direct characteristic polynomial solution failed.")
    print("Eigenvalues computation using .eigenvals() succeeded.")
    
if __name__ == "__main__":
    test_eigenvalues_computation()
```

When executed with `python3 reproducer.py`, this script will attempt to find the eigenvalues of the symbolic matrix using `.eigenvals()`. If that fails, the script tries a direct approach by solving the characteristic polynomial. The assertion is designed to trigger if these methods do not produce the expected results, particularly focusing on the failure of `.eigenvals()` while being able to find solutions directly. The script exits with code 0 only if the `.eigenvals()` method succeeds, aligning with your criteria for determining whether the issue has been resolved.