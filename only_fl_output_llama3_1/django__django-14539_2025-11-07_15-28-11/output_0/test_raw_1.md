Here is the reproducer script:

```python
import re
from urllib.parse import unquote, quote

def urlize(s):
    s = re.sub(r'([a-zA-Z0-9_\-\.])', r'<a href="http://\1">', s)
    return s

def test_urlize():
    assert urlize('Search for google.com/?q=1&lt! and see.') == 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'

try:
    test_urlize()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Test passed. Issue is fixed.")
    exit(0)

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

if __name__ == '__main__':
    test_urlize()
```

This script will run the `urlize` function and assert that it produces the expected output. If the assertion fails, it will raise an `AssertionError`, which will be caught by the script and printed with a stack trace.