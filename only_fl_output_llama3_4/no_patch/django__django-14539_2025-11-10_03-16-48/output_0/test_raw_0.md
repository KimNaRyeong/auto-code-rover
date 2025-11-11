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
        urlized_string = urlize.urlize('Search for google.com/?q=1&lt! and see.')
        assert "lt!" in unquote(urlized_string), f"Expected 'lt!' to be present, but got {unquote(urlized_string)}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `urlize` function with the given input and check if the expected output is correct. If not, it will raise an `AssertionError`, which will be caught by the script and printed to the console along with a stack trace. The script then exits with code 1.