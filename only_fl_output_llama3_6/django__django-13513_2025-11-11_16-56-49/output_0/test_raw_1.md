Here is the reproducer script:

```python
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

def test_issue():
    try:
        raise RuntimeError('my error')
    except Exception as exc:
        raise ValueError('my new error') from None

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue fixed. Exiting with code 0.")
    sys.exit(0)
```

This script raises a `RuntimeError` and then catches it, re-raising a `ValueError`. The issue is that the debug error view doesn't respect `exc.__suppress_context__`, so the original `RuntimeError` should be shown in the traceback.