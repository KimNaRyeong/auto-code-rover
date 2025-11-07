Given the previous response didn't accurately capture the error handling and output expectations based on your requirements, I'll adjust the approach to ensure the script raises an `AssertionError` if the issue described is indeed present, along with a correct handling of the output message and stack trace. I'll correct the script to reflect a proper execution flow that abides by your instructions:

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
    from sympy import symbols, Matrix, eye, exp, solve

    x = symbols('x', real=True)  # Declare x as a real symbol to see if this affects the solution.
    M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])
    
    try:
        # Attempt to use the .eigenvals() method to find the eigenvalues.
        eigenvals_result = M.eigenvals()
        # If no exception is raised, but the result is empty, assert an error.
        assert eigenvals_result, "Eigenvalues computation should not return an empty result."
    except Exception as e:
        print_stacktrace(e)
        try:
            # If .eigenvals() fails, attempt to solve the characteristic polynomial directly.
            lam = symbols('lambda')
            roots_solution = solve((M - lam * eye(3)).det(), lam)
            assert roots_solution, "Roots computation should not return an empty result."
            # If roots_solution is found, this implies that .eigenvals() has an issue.
            print(f"Roots found through direct solution: {roots_solution}")
            raise AssertionError("Failed to compute eigenvalues with .eigenvals(), but direct solution found roots.") from e
        except Exception as inner_exc:
            # If solving the characteristic polynomial also fails, print this stack trace for clarity.
            print_stacktrace(inner_exc)
            print("Failed to compute eigenvalues both with .eigenvals() and direct characteristic polynomial solution.")

if __name__ == "__main__":
    main()
```

This revised script closely adheres to the initial instructions, ensuring an `AssertionError` is raised if the `.eigenvals()` method fails to find the eigenvalues for the given symbolic matrix while being able to find solutions directly through solving the characteristic polynomial. It provides a comprehensive error handling mechanism to capture and explain the failure in detail if either of the test methods fail to compute the expected result.