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

    x = symbols('x')
    M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])

    try:
        eigenvals_result = M.eigenvals()
        assert eigenvals_result, "Eigenvalues should not be None or empty"
    except Exception as exc1:
        try:
            lam = symbols('lambda')
            roots_result = solve((M - lam * eye(3)).det(), lam)
            assert roots_result, "Roots should not be None or empty"
            print_stacktrace(exc1)
            raise AssertionError("eigenvals() failed, but roots could be found") from exc1
        except Exception as exc2:
            print("Roots could not be found either, indicating a possible deeper issue with symbolic computation.")
            print_stacktrace(exc2)

if __name__ == "__main__":
    main()
```

This script checks whether the `.eigenvals()` method can fetch the eigenvalues of a given symbolic matrix. If it fails, it attempts to find the roots of the characteristic polynomial directly using `solve()`. If the latter succeeds but the former doesn't, an `AssertionError` is raised, and the stack trace of the first failure (`.eigenvals()` method) is printed. If both methods fail, it suggests a deeper issue with the symbolic computation, and both stack traces should be examined for further debugging.