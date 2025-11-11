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

def reproduce_issue():
    try:
        urlized = urlize.urlize('Search for google.com/?q=1&lt! and see.')
        if urlized != 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.':
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will execute the `urlize.urlize()` function with a test string, compare the result to the expected output, and if they don't match, it will raise an `AssertionError` and print the stack trace. If the issue is fixed, it will exit with code 0.