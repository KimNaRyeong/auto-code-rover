 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.ensemble import AdaBoostClassifier
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    clf = AdaBoostClassifier(base_estimator=None)
    try:
        clf.fit([[1]], [0])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should raise an `InvalidParameterError` with a stack trace, indicating that the issue is present. The line numbers of the statements may differ depending on the specific version of scikit-learn being used.