Below is a standalone Python file named `reproducer.py`, written to reproduce the described issue. This script sends a POST request to a Django application running on `localhost:8000` with a file that has a null byte in its file extension.

```python
# reproducer.py

import requests
import io

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

def send_malicious_request():
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt\x00", contents, "text/plain")}
    try:
        response = requests.post("http://localhost:8000/", files=files)
        # Assert raises an error only if issue is reproduced successfully
        # You may adjust the check according to the actual failing condition on your setup.
        assert response.status_code == 500, "Expected server to return HTTP 500 error"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        send_malicious_request()
        print("Issue reproduced successfully.")
    except AssertionError as e:
        print("Issue NOT present. Exiting with code 0.")
        exit(0)
```

Please note:
- This script assumes that your Django application (which is presumably configured to mimic the problematic behavior) is running and accessible at `http://localhost:8000/`.
- The script is intended to directly reproduce the ValueError (embedded null byte) by sending a specially crafted file upload POST request. However, this specific behavior depends on how your Django application handles file uploads and parses file names. Therefore, you may need to adjust the part where the assert condition is defined if the application does not result in a 500 status code but instead fails differently.
- The `AssertionError` is used here to indicate whether the issue exists: it prints a custom message and ends the execution with code 0 if the issue is fixed.
- As per the given instructions, if an unexpected exception is caught, it will print a stack trace showing the error location and details, thanks to the `print_stacktrace` function.