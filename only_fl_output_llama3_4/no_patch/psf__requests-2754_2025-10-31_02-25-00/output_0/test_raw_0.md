Here is the reproducer script:

```python
import requests
from urllib.parse import urlparse, urlunparse
import sys
import traceback

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
    url = 'http://test.xn--q9jyb4c'
    redirect_url = '/index.html'
    target_url = '/ブログ'

    response = requests.get(url + redirect_url, allow_redirects=False)
    if response.status_code == 404:
        print_stacktrace(response.exceptions.RequestException())
        sys.exit(1)

    new_url = urlparse(response.headers['Location'])
    new_path = urlunparse((new_url.scheme, new_url.netloc, target_url, '', ''))
    if new_path != url + target_url:
        print_stacktrace(AssertionError('Redirect failed to point to the expected URL'))
        sys.exit(1)

reproduce_issue()
```

This script sends a GET request to the specified URL with the redirect, checks if the response status code is 404 (which should happen when the redirect fails), and then checks if the Location header points to the expected URL. If either of these conditions fail, it prints the stack trace and exits with code 1.