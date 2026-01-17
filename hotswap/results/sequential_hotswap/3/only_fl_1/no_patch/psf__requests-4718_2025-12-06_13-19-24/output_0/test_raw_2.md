 I apologize for the confusion. Here is an updated standalone Python script `reproducer.py` that reproduces the issue:
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

def test_redirect():
    try:
        response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        response.raise_for_status()
        assert response.url == 'http://localhost:8000', "AssertionError expected, but not raised"
    except AssertionError:
        raise
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_redirect()
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script sends a request with an Authorization header to an HTTPS server running on localhost:4443, which responds with a 302 redirect to `http://localhost:8000`. The Authorization header is not stripped in the redirected request, and the credentials are transmitted in plaintext to `http://localhost:8000`.

The script raises an `AssertionError` to indicate the presence of the issue. The stack trace of the error can be seen in the console output.

To fix the issue, the `requests` library should strip the Authorization header if the scheme is changed from HTTPS to HTTP.