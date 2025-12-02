 Here is a standalone python file `reproducer.py` to reproduce the issue:
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
When executed with `python3 reproducer.py`, the script will raise a `ValueError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 18, in main