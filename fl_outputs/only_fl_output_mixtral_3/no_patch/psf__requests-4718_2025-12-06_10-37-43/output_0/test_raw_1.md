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

def run_test():
    try:
        https_server = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        assert https_server.status_code == 302

        http_server = requests.get(https_server.headers['Location'], auth=('hello', 'world'), verify=False)
        assert http_server.status_code == 200

        # Assert that the Authorization header is not present in the HTTP request
        assert 'Authorization' not in http_server.request.headers

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    run_test()
```
This script uses the `requests` library to make HTTP requests to the servers specified in the issue description. It first sends a request to the HTTPS server, which should return a 302 redirect response. The script then sends a request to the HTTP server specified in the `Location` header of the 302 response. If the `Authorization` header is present in the HTTP request, the script raises an `AssertionError` and prints a stack trace.

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, the script will print a stack trace and exit with code 1. If the issue is fixed, the script will exit with code 0.