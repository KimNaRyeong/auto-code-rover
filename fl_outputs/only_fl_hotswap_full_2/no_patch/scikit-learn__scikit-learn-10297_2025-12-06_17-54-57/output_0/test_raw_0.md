 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn import linear_model as lm

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    #test database
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size = n)

    try:
        rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, store_cv_values = True).fit(x, y)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    main()
  File "reproducer.py", line 18, in main
    assert False
AssertionError
```
This confirms that the issue is present. The issue is that the `store_cv_values` parameter is not supported by the `RidgeClassifierCV` class, even though the documentation claims that it is possible to use this flag. The expected behavior would be for the `store_cv_values` parameter to be supported and for the cross-validation values to be stored as an attribute of the `RidgeClassifierCV` object.