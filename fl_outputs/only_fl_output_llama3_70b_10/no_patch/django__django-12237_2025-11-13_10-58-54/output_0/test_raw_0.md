Here is the standalone Python script `reproducer.py` to reproduce the issue:
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
    assert re.match(r'^[-\w]+$', slug), f"Invalid slug: {slug}"

try:
    test_slugify()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script uses the `slugify` function from Django to generate a slug for the title "Hello İstanbul". It then checks if the generated slug matches the expected pattern using a regular expression. If the slug is invalid, it raises an `AssertionError`, which is caught and printed with a stack trace using the provided `print_stacktrace` function.