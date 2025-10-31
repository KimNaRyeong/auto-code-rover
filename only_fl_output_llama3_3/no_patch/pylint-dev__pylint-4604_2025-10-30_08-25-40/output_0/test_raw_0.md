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
        Run(['--rcfile=/dev/null', '--disable=unused-import'])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Issue not reproduced")
    else:
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script runs Pylint with the `--rcfile=/dev/null` option to disable all checks except for the one we're interested in (unused-import), and then it checks if the exit code is 0. If the issue is present, an AssertionError will be raised with a stack trace printed using the provided function.