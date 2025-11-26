Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import unicodedata
import re
from django.utils.text import slugify

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

def test_slugify():
    title = "Hello İstanbul"
    slug = slugify(title, allow_unicode=True)
    try:
        assert re.match(r'^[-\w]+$', slug), f"Invalid slug: {slug}"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_slugify()
```
This script will reproduce the issue by attempting to slugify the string "Hello İstanbul" with `allow_unicode=True`. If the resulting slug is invalid, it will raise an `AssertionError` and print a stack trace of the issue.