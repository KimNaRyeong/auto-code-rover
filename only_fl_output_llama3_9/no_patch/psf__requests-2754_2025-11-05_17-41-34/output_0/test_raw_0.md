Here is the reproducer script:

```python
import requests
import sys
from urllib.parse import urlparse, urlunparse

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

    response = requests.get(url + redirect_url, allow_redirects=True)
    if response.status_code == 404:
        print_stacktrace(response.exceptions.RequestException())
        sys.exit(1)

    assert response.url == urlunparse(urlparse(url)._replace(path=target_url)), f"Expected {url}{target_url}, got {response.url}"
    print(f"Issue reproduced successfully. Expected URL: {url}{target_url}")

if __name__ == "__main__":
    reproduce_issue()
```

This script sends a GET request to the specified URL, which should redirect to the target URL. If the response status code is 404, it prints the stack trace and exits with code 1. Otherwise, it asserts that the actual URL matches the expected URL and prints a success message if the assertion passes.