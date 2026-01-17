 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import requests
import sys

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
    original_request = requests.Request('POST', 'http://server.example.com/do_something')
    prepped_request = original_request.prepare()
    session = requests.Session()
    response = session.resolve_redirects(prepped_request)
    for resp in response.history:
        if resp.status_code == 303:
            assert resp.request.method == 'POST', 'The method of the request should be POST'
        elif resp.status_code == 307:
            assert resp.request.method == 'GET', 'The method of the request should be GET'

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present, and exit with code 1. If the issue is fixed, the script will exit with code 0.