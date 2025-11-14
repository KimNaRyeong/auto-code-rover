Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import requests
from urllib3 import version as urllib3_version
from OpenSSL import version as pyopenssl_version

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

def test_pyopenssl_redirect():
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get('https://httpbin.org/status/301')
        if response.status_code == 301:
            assert False, "Exception not raised when getting a 301 response to a HTTPS request"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Exception raised when getting a 301 response to a HTTPS request")

if __name__ == "__main__":
    print(f"urllib3 version: {urllib3_version}")
    print(f"pyOpenSSL version: {pyopenssl_version}")
    test_pyopenssl_redirect()
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.

Please note that I added a check for the status code of the response to ensure that we are actually getting a 301 response before asserting that an exception should be raised.

You can run this script using `python3 reproducer.py`.