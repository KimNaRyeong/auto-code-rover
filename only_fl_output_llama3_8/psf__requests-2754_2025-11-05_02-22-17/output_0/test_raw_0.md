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
    url = 'http://test.みんな'
    redirect_url = '/index.html'

    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 301:
            new_url = urlparse(response.url)
            new_url = list(new_url)
            new_url[2] = redirect_url
            new_url = urlunparse(new_url)
            response = requests.get(new_url)
            print_stacktrace(response.raise_for_status())
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script sends a GET request to the specified URL, then checks if the response is a redirect (301). If it is, it constructs the new URL by replacing the path with the redirect URL and sends another GET request. It then prints the stack trace of any exception that occurs during this process.

To run the script, save it in a file named `reproducer.py` and execute it using `python3 reproducer.py`.