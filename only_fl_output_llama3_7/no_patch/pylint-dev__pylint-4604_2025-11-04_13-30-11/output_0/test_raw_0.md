Here is the reproducer script:

```python
import astroid
from pylint.lint import Run

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
        Run(['--rcfile=/dev/null', 'a.py'])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Issue not reproduced")
    else:
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `pylint` command on a file named `a.py`, which contains the code that reproduces the issue. If the issue is present, it will raise an `AssertionError`.