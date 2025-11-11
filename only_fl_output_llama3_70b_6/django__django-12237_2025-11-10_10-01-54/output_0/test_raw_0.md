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
    assert re.match(r'^[-\w]+$', slug), f"Invalid slug: {slug}"

try:
    test_slugify()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` when the issue is present, printing a stack trace of the issue. If the issue is fixed, it will exit with code 0.

To run this script, save it to a file named `reproducer.py` and execute it with `python3 reproducer.py`.