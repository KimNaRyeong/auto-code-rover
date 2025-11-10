Here is the reproducer script:

```python
import unittest
from django.test import RequestFactory, TestCase
from django.views.i18n import set_language
from urllib.parse import urlparse, unquote

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

class Reproducer(unittest.TestCase):
    def test_set_language_url_params(self):
        rf = RequestFactory()
        request = rf.post("", next="")
        request.META['HTTP_REFERER'] = '/someurl/?paramter=some%20%26%20thing'
        response = set_language(request)
        if urlparse(response.url).query != unquote('/someurl/?paramter=some%20%26%20thing'):
            raise AssertionError("Expected URL to be the same, but got: " + response.url)

if __name__ == '__main__':
    try:
        unittest.main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script should reproduce the issue and print a stack trace when an `AssertionError` is raised.