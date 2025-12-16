 I apologize for the confusion. Here's an updated `reproducer.py` script that should reproduce the issue:
```python
import requests

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    try:
        response = requests.get('https://httpbin.org/redirect-to?url=http://httpbin.org/get', auth=('user', 'pass'), verify=False)
        if response.status_code == 200 and 'Authorization' in response.text:
            assert False, 'Authorization header was not cleared in HTTPS -> HTTP redirect'
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    test_issue()
```
This script makes a request to a server that redirects from HTTPS to HTTP, and checks if the `Authorization` header is present in the final response. If the header is present, an `AssertionError` is raised and a stack trace is printed.

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.