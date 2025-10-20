Here's a Python script `reproducer.py` that follows your specifications to reproduce the issue described. This script sends a POST request to the Django server with a file containing a null character in its extension. If the issue is present, it will raise an `AssertionError`, and it attempts to print the stack trace of the issue using the provided `print_stacktrace` function. The script will exit with code 0 if the issue is fixed.

```python
import requests
import io
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def send_malformed_file_request():
    contents = io.StringIO("." * (1024 * 1024 * 3))  # Creating a 3MB file
    files = {"docfile": (b"bogus.txt\0", contents, "text/plain")}  # Filename contains null byte
    try:
        response = requests.post("http://localhost:8000/", files=files)
        assert response.status_code == 400, "Expected a 400 error due to malformed filename"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code if an unexpected error occurs
    else:
        print("Issue fixed. Exiting with code 0.")
        sys.exit(0)  # Exit with code 0 if the issue is fixed

if __name__ == "__main__":
    send_malformed_file_request()
```

Please note the following:
- This script assumes that the Django application is running on `http://localhost:8000/`.
- The script currently anticipates receiving a 400 HTTP status code for a malformed filename with a null byte, as per the described fix scenario. However, the handling might need adjustment based on the actual implementation of the fix in your Django application.
- Ensure that the server is correctly set up to handle POST requests and that any required CSRF token handling or session authentication is appropriately configured for this test to work. This example uses `@csrf_exempt` to bypass CSRF token verification for simplicity, but in a real-world scenario, CSRF protection should not be disabled.