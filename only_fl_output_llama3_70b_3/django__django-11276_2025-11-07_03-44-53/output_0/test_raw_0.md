Here is the `reproducer.py` file that reproduces the issue:
```
import timeit
from django.utils.html import escape as django_escape
import html

def test_django_escape():
    copyright = 'Copyright 2023'
    result = django_escape(copyright)
    assert result == 'Copyright &#39;2023', f"Expected '&#39;', but got '{result}'"

def test_html_escape():
    copyright = 'Copyright 2023'
    result = html.escape(copyright)
    assert result == 'Copyright &#x27;2023', f"Expected '&#x27;', but got '{result}'"

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
    test_django_escape()
    test_html_escape()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed")
exit(0)
```
This script tests both the `django.utils.html.escape()` function and the `html.escape()` function with a sample input. If the issue is present, it raises an `AssertionError` with a message indicating the expected and actual results. The `print_stacktrace()` function is used to print the stack trace of the error.

If the issue is fixed, the script prints "Issue is fixed" and exits with code 0.