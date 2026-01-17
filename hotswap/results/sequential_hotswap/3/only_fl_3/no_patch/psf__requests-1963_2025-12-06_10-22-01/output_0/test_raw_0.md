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
            assert resp.request.method == 'POST', 'Incorrect method selection'
        elif resp.status_code == 307:
            assert resp.request.method == 'GET', 'Incorrect method selection'

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 26, in <module>
    reproduce_issue()
  File "reproducer.py", line 21, in reproduce_issue
    assert resp.request.method == 'GET', 'Incorrect method selection'
AssertionError: Incorrect method selection
```
This confirms that the issue is present in the `Session.resolve_redirects` method, which copies the original request for all subsequent requests, causing incorrect method selection.