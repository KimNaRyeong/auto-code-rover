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
    # Add your code that reproduces the issue here
    from Schur_Number import Schur_Number  # Replace 'Schur_Number' with the actual module name
    Schur_Number()
    self.fail("Expected AssertionError")
except AssertionError as e:
    print_stacktrace(e)
```

Please replace `'Schur_Number'` with the actual module name where you have defined `Schur_Number`.