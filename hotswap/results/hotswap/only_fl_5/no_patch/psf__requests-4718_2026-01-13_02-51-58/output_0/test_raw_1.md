 Here's a standalone Python script `reproducer.py` that reproduces the issue:
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
        if 'Authorization' in https_server.request.headers:
            raise AssertionError('Authorization header should have been cleared in the HTTPS to HTTP redirect')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    run_test()
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.

Note: The provided script assumes that there is an HTTPS server running on localhost:4443 and a plain HTTP server (or netcat) running on localhost:8000, as described in the reproduction steps. The HTTPS server should reply with a 302 redirect to `http://localhost:8000`. The script uses the `requests` library to make the HTTPS request and check the headers of the response. If the `requests` library is not installed, it can be installed using pip:
```
pip install requests
```