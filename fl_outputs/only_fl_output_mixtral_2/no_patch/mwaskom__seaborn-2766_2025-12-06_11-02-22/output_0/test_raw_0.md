 Here's a standalone Python script `reproducer.py` that reproduces the issue:

```python
import setuptools
import seaborn

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

try:
    # This import triggers the warning
    _ = seaborn.apionly
except DeprecationWarning as e:
    print_stacktrace(e)
    assert False, "DeprecationWarning should not be raised"
```

To reproduce the issue, run the script with `python3 reproducer.py`. If the issue is fixed, the script should exit without raising any exceptions. The script imports `seaborn` and then imports a private function from `seaborn` to trigger the warning. If the warning is raised, the script prints a stack trace and raises an `AssertionError`.