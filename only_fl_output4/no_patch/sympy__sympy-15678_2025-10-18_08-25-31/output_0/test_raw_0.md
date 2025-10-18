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

def main():
    from sympy import symbols, Eq, exp, idiff

    x = symbols('x')
    y, f = symbols('y f', cls=symbols.Function)

    try:
        # Check for Eq support
        eq_result = idiff(Eq(y(x)*exp(y(x)), x*exp(x)), y(x), x)
        raise AssertionError("idiff() should not have succeeded with Eq objects")
    except Exception as e:
        print_stacktrace(e)

    try:
        # Check for function support
        func_result = idiff(f(x)*exp(f(x)) - x*exp(x), f(x), x)
        raise AssertionError("idiff() should not have succeeded with function objects")
    except Exception as e:
        print_stacktrace(e)

    try:
        # Verify if the original use case without Eq or f(x) is working
        correct_result = idiff(y*exp(y) - x*exp(x), y, x)
        assert str(correct_result) == "(x + 1)*exp(x - y)/(y + 1)", "Expected different outcome"
        print("No AssertionError encountered, issue seems to be fixed.")
        exit(0)
    except AssertionError as e:
        print(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script checks for three conditions based on your problem statement:
1. It first attempts to execute `idiff` with an equation wrapped inside an `Eq` object, which is expected to fail with the described issue.
2. Then, it tries to pass `f(x)` as part of the equation, which is also supposed to trigger the described failure.
3. Finally, it checks if `idiff` can correctly solve an expression without using `Eq` objects and `f(x)`, which should work as per your last example.

The script utilizes assertions to check for the presence of the issues. When executed under the conditions that reproduce the problem, the `AssertionError`s will be skipped due to the exceptions being caught first, and it will print the relevant stack traces. When the issues are fixed, no exception relating to the problem should occur, and the script exits normally with code 0 if everything is correct.
