Here is the reproducer script:

```python
import urlize
from unittest import TestCase

class Reproducer(TestCase):
    def test_urlize(self):
        self.assertEqual(urlize.urlize('Search for google.com/?q=1&lt! and see.'),
                         'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.')

if __name__ == '__main__':
    try:
        Reproducer().test_urlize()
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

```

This script will run the test case and if it fails, it will print the stack trace of the failure.