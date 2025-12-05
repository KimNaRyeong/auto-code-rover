 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    from sklearn.linear_model import RidgeCV
    from sklearn.datasets import make_regression

    X, y = make_regression()
    ridge = RidgeCV(alphas=[1, 10, 100, 1000]).fit(X, y)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will reproduce the issue and print a stack trace of the error. The error message and stack trace will be written to the standard error stream, and the script will exit with a non-zero exit code.

To fix the issue, you can modify the `alphas` parameter to contain at least one floating-point value, for example:
```python
ridge = RidgeCV(alphas=[1.0, 10, 100, 1000]).fit(X, y)
```
This will avoid the `ValueError` and allow the script to execute without errors.