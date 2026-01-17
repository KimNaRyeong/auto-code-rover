 Here is a corrected standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    clf = make_pipeline(LogisticRegression())
    try:
        clf.fit([[0], [0]], [0, 1], sample_weight=[1, 1])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error message is not friendly enough"

if __name__ == "__main__":
    main()
```
When executed by `python3 reproducer.py`, it will raise an `AssertionError` with the stack trace of the issue. The error message is not friendly enough, and it should explicitly describe the correct format for passing `sample_weight` to a step in a `Pipeline`.