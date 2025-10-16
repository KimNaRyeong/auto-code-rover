Certainly! Here's a standalone Python script named `reproducer.py` designed to reproduce the issue described. When executed, it attempts to perform an HTTP request that redirects to an HTTPS URL, which then triggers the issue with the `pyOpenSSL` library due to the type mismatch of the URL being passed. The script will catch the exception, print a detailed stack trace as requested, and assert the presence of the issue. When the underlying issue with the libraries is resolved, the script should terminate without errors, assuming no `AssertionError` is raised.

```python
import requests
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

def main():
    try:
        # Attempt to make a request that will redirect from HTTP to HTTPS,
        # which is expected to trigger the issue when handled by pyOpenSSL.
        response = requests.get('https://httpbin.org/status/301')
        # If the request completes without raising an error, the issue is assumed to be resolved.
        print("Request completed successfully. The issue seems to be resolved.")
    except Exception as e:
        print_stacktrace(e)
        # Raising an AssertionError to indicate the issue is present.
        # Modify this behavior as needed based on how you wish to handle detection
        # of the issue vs. its resolution.
        raise AssertionError("The issue with pyOpenSSL/SNI and 301 redirects is present.") from e

if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(error)
        sys.exit(1)  # Exit with a non-zero code to indicate failure due to the issue being present.
    else:
        sys.exit(0)  # Exit with 0 to indicate the issue is not present/resolved.
```

Make sure to adjust the behavior inside the `main()` function based on your specific debugging or logging requirements. This script emphasizes catching and diagnosing the problematic interaction with the `pyOpenSSL` library.