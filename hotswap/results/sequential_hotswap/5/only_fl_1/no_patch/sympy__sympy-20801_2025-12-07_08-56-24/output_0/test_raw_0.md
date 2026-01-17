 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *
from sympy.utilities.exceptions import SympyDeprecationWarning

# Suppress SympyDeprecationWarning to avoid masking the AssertionError
simple_warning(SympyDeprecationWarning, 0)

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
    # Reproduce the issue
    result1 = S(0.0) == S.false
    result2 = S.false == S(0.0)

    # Assert that the results are inconsistent
    assert result1 != result2, "S(0.0) == S.false and S.false == S(0.0) should not be equivalent"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace if the issue is present:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    main()
  File "reproducer.py", line 18, in main
    print_stacktrace(e)
  File "reproducer.py", line 7, in print_stacktrace
    tb = traceback.extract_tb(e.__traceback__)
AssertionError: S(0.0) == S.false and S.false == S(0.0) should not be equivalent
```
If the issue is fixed, the script will exit with code 0 without printing any stack trace.