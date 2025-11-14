Here is the `reproducer.py` file that reproduces the issue:
```python
import requests

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

def test_linkcheck():
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    headers = {"User-Agent": "Sphinx/2.4.3 requests/2.23.0 python/3.7.4"}
    
    # Reproduce the issue with hardcoded Accept header
    response = requests.head(url, headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    # Try with custom Accept header to demonstrate the fix
    headers["Accept"] = "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"
    response = requests.head(url, headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

try:
    test_linkcheck()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script sends a `HEAD` request to the specified URL with the hardcoded `User-Agent` header and checks that the response status code is 200. Then, it tries again with a custom `Accept` header to demonstrate how the issue can be fixed.

If the issue is present, the script will raise an `AssertionError` and print a stack trace of the error. If the issue is fixed, the script will exit with code 0.