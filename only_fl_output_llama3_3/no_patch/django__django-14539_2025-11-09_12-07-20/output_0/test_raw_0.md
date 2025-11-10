Here is the reproducer script:

```python
import urlize
from urllib.parse import unquote

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
    urlized_string = urlize.urlize('Search for google.com/?q=1&lt! and see.')
    if urlized_string != 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.':
        raise AssertionError("urlize() does not handle html escaped string and trailing punctuation correctly")
except Exception as e:
    print_stacktrace(e)
    exit(0)
```

This script will run the `urlize.urlize()` function with a test string, check if the output matches the expected output, and if it doesn't, raise an `AssertionError`. If an error occurs during this process, it will print the stack trace using the provided `print_stacktrace()` function.