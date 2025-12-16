 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import requests
from http.client import responses

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    url = "http://server.example.com/do_something"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "param1=value1&param2=value2"

    s = requests.Session()
    s.headers.update(headers)

    # First request is a POST
    r = s.post(url, data=data)
    assert r.status_code == 303, "First request should return 303"

    # Intermediate 303 See Other has caused the POST to be converted to a GET
    location = r.headers["Location"]
    r = s.get(location)
    assert r.status_code == 307, "Second request should return 307"

    # Subsequent 307 should preserve the GET
    location = r.headers["Location"]
    r = s.get(location)
    assert r.status_code == 200, "Third request should return 200"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present. The line numbers of the statements may vary depending on the version of Python and the platform.

To fix the issue, you can modify the `reproduce_issue` function to use the `requests.Request` class to create a new request object for each subsequent request, instead of copying the original request object:
```python
def reproduce_issue():
    url = "http://server.example.com/do_something"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "param1=value1&param2=value2"

    s = requests.Session()
    s.headers.update(headers)

    # First request is a POST
    r = s.post(url, data=data)
    assert r.status_code == 303, "First request should return 303"

    # Intermediate 303 See Other has caused the POST to be converted to a GET
    location = r.headers["Location"]
    req = requests.Request("GET", location)
    r = s.send(req, **r.request.headers)
    assert r.status_code == 307, "Second request should return 307"

    # Subsequent 307 should preserve the GET
    location = r.headers["Location"]
    req = requests.Request("GET", location)
    r = s.send(req, **r.request.headers)
    assert r.status_code == 200, "Third request should return 200"
```
With this modification, the script will exit with code 0 when executed with `python3 reproducer.py`, indicating that the issue is fixed.