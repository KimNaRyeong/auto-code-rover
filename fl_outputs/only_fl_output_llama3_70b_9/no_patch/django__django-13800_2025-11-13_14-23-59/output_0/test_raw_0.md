Here is a standalone Python script `reproducer.py` to reproduce the issue:
```
import os
from django.contrib.messages import get_messages
from django.http import HttpResponse

def reproducer():
    response = HttpResponse()
    messages = get_messages(response.wsgi_request)
    messages.add_message(1, "123\\\"NOTRECEIVED\"")
    
    cookie_value = response.cookies['messages'].value
    assert '\\' not in cookie_value, f"Cookie value contains escape character: {cookie_value}"
    
    print("Issue is fixed!")

try:
    reproducer()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

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

if __name__ == "__main__":
    reproducer()
```
This script uses the `django.contrib.messages` module to add a message with an escape character in its value. It then checks if the resulting cookie value contains the escape character, and raises an `AssertionError` if it does. If the issue is fixed, the script prints "Issue is fixed!" and exits with code 0.