The issue is not with the RidgeClassifierCV class itself, but rather with the installation of scikit-learn. The error message indicates that the package has not been built correctly.

To reproduce this issue, you would need to install scikit-learn from source and then run your reproducer script. Here's an example of how you could do it:

```python
import sys

def print_stacktrace(e):
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
    try:
        from sklearn.linear_model import RidgeClassifierCV
        rr = RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, store_cv_values=True).fit(np.random.randn(100, 30), np.random.normal(size=100))
    except ImportError as e:
        print_stacktrace(e)
        raise AssertionError("Expected ImportError")
    else:
        assert False, "Expected ImportError"

if __name__ == '__main__':
    main()
```

This script will attempt to import the RidgeClassifierCV class from scikit-learn. If the installation of scikit-learn is not correct, it will raise an ImportError and print a stack trace.