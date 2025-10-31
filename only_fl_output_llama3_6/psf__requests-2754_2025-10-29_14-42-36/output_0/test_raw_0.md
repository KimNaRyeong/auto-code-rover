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
    url = 'http://test.みんな'
    redirect_url = '/index.html'
    target_url = '/ブログ'

    response = requests.get(url, allow_redirects=False)
    if response.status_code == 301:
        new_url_parts = list(urlparse(response.headers['Location']))
        new_url_parts[2] = target_url
        new_url = urlunparse(new_url_parts)
        print(f"Redirecting from {url} to {new_url}")
        response = requests.get(new_url, allow_redirects=False)
    else:
        print("No redirect found")
        return

    if response.status_code == 404:
        raise AssertionError("Issue reproduced")

    print_stacktrace(sys.exc_info()[1])

if __name__ == "__main__":
    reproduce_issue()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.