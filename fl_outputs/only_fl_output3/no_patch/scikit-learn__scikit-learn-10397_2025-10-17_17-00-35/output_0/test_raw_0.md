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

def test_issue():
    from sklearn.linear_model import RidgeCV
    from sklearn.datasets import make_regression

    try:
        X, y = make_regression()
        ridge = RidgeCV(alphas=[1, 10, 100, 1000]).fit(X, y)
    except ValueError as e:
        if "Integers to negative integer powers are not allowed." in str(e):
            print_stacktrace(e)
            raise AssertionError("Issue present: Integers in RidgeCV alpha cause ValueError.") from e

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print(e)
        exit(1)
    print("Issue is fixed.")
    exit(0)
```