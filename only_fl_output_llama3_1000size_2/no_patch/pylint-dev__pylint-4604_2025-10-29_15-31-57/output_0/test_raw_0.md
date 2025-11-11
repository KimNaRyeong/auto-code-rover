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
        Run(["-E", "W0611", "-d", "a"])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Issue not reproduced")
    else:
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script runs Pylint with the `-E` option to enable error output, and the `W0611` warning to check for unused imports. It then checks if the exit code is 0 (indicating no errors were found). If not, it raises an `AssertionError`.