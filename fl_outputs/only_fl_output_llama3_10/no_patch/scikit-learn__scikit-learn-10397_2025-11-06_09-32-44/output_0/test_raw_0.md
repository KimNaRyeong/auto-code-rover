Here is the reproducer script:

```python
import sys
from sklearn.linear_model import RidgeCV
from sklearn.datasets import make_regression

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
    try:
        X, y = make_regression()
        ridge = RidgeCV(alphas=[1, 10, 100, 1000]).fit(X, y)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
    sys.exit(0)
```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3.6: `python3 reproducer.py`. This should print the stack trace of the issue and raise an AssertionError.