Here is the reproducer script:

```python
import urlize

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
    urlized = urlize.urlize('Search for google.com/?q=1&lt! and see.')
    assert urlized == 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.', "urlize() does not handle html escaped string and trailing punctuation correctly"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed!")
exit(0)
```

This script will run the `urlize` function with a test input, check if the output matches the expected result using an assertion statement, and raise an `AssertionError` if it doesn't. If an error occurs during this process, it will print the stack trace using the provided `print_stacktrace` function and exit with code 1.