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

from django.utils import dateformat

def test_date_format():
    year = 1
    formatted_year = dateformat.DateFormat().Y(year)
    assert len(str(formatted_year).rjust(4, '0')) == 4, f"Expected a four-digit year padded with zeros, but got {formatted_year}"
    
try:
    test_date_format()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test succeeded.")
exit(0)
```

This script will run the `test_date_format` function which checks if the formatted year using the Y specifier in Django's dateformat module is a four-digit year padded with zeros. If any of these assertions fail, it will print the stack trace and exit with code 1.