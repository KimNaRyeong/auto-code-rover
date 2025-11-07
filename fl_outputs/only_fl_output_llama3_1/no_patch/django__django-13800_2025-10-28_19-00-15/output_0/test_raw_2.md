Here is the reproducer script:

```python
import http.cookies
from django.utils.http import cookie_to_morsel, quote_cookie_value

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
    cookie_value = 'messages=\"123\\\"NOTRECEIVED\"'
    try:
        morsel = cookie_to_morsel(quote_cookie_value(cookie_value))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to create a cookie using the `cookie_to_morsel` and `quote_cookie_value` functions from Django. The provided cookie value is not RFC 6265 compliant (it contains an escape character). If the issue is present, it will raise an exception and print the stack trace using the provided function.