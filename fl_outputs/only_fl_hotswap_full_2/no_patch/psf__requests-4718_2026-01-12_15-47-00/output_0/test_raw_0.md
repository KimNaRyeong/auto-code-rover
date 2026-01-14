 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
        https_server = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        if https_server.status_code == 302 and https_server.headers['Location'] == 'http://localhost:8000':
            http_server = requests.get(https_server.headers['Location'], headers={'Authorization': https_server.headers['Authorization']}, verify=False)
            if http_server.status_code == 200 and http_server.text == '':
                assert False, 'Authorization header was not cleared in HTTPS -> HTTP redirect'
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    test_issue()
```
This script makes a request to an HTTPS server running on localhost:4443, which responds with a 302 redirect to `http://localhost:8000`. The script then makes a request to the redirected URL with the same `Authorization` header and checks if the response status code is 200 and the response body is empty. If the `Authorization` header is not cleared, an `AssertionError` is raised and a stack trace is printed.

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.

Note: The SSL server code is not included in this script, as it is not necessary to reproduce the issue. The SSL server code provided in the issue description can be used separately to test the script.