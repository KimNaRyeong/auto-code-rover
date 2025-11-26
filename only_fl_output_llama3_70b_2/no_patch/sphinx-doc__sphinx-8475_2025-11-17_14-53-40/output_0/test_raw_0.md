Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import requests
from urllib.parse import urlparse

def check_link(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.TooManyRedirects:
        # This is where the issue occurs, we should retry with a GET request
        print("TooManyRedirects exception caught, but not retried with GET")
        raise AssertionError("Link checking failed due to TooManyRedirects")

def main():
    url = "https://idr.openmicroscopy.org/webclient/?show=well-119093"
    if not check_link(url):
        raise AssertionError("Link is broken")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
This script will raise an `AssertionError` when the issue is present, and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

You can run this script by executing `python3 reproducer.py` in the root directory of the project.