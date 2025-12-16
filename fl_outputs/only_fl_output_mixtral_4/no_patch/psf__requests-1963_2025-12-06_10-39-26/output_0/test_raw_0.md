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
    session = requests.Session()
    original_request = requests.Request('POST', 'https://server.example.com/do_something')
    prepared_request = session.prepare_request(original_request)
    response = session.send(prepared_request, allow_redirects=True)
    if response.request.method != 'GET':
        raise AssertionError(f"Expected GET request, got {response.request.method} instead")

if __name__ == '__main__':
    try:
        reproduce_issue()
        print("Issue not present")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script will print "Issue not present" and exit with code 0.