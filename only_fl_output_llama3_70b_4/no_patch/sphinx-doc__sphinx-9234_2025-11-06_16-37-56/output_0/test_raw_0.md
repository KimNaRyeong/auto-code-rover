Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import requests
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

def check_redirect(url, expected_url):
    response = requests.head(url, allow_redirects=True)
    if response.url != expected_url:
        raise AssertionError(f"Redirect from {url} to {response.url} is not allowed")

try:
    # Test case 1: Allowed redirect
    url = "https://www.sphinx-doc.org/"
    expected_url = "https://www.sphinx-doc.org/en/master/"
    check_redirect(url, expected_url)

    # Test case 2: Disallowed redirect (issue reproduction)
    url = "https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/"
    expected_url = "https://blogs.windows.com/windowsdeveloper/2016/12/02/symlinks-windows-10/"  # Should raise AssertionError
    check_redirect(url, expected_url)

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script sends a HEAD request to the specified URLs and checks if the redirect URL matches the expected URL. If not, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.