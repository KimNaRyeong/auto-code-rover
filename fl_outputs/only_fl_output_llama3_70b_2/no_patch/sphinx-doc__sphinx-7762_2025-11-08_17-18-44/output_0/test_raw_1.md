I apologize for the mistake. Here is a new `reproducer.py` script that should reproduce the issue:
```python
import sys
import urllib.request

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
    req = urllib.request.Request(url, headers={'User-Agent': 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4'})
    response = urllib.request.urlopen(req)
    assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"

if __name__ == "__main__":
    try:
        test_linkcheck()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script uses the `urllib.request` module to send a request to the specified URL with the hardcoded `User-Agent` header and checks if the response status code is 200. If not, it raises an `AssertionError` with a message indicating the expected and actual status codes.

When run, this script should reproduce the issue and print a stack trace of the error.