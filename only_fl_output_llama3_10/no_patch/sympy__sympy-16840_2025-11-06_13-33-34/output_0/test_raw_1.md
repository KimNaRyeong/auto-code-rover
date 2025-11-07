Here is the reproducer script:

```python
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

try:
    result = 2 // 0.5
    assert type(result) == int, "Expected integer but got {}".format(type(result))
except Exception as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed")
    exit(0)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, it will print "Issue is fixed" and exit with code 0.