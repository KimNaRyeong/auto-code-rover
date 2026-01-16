```python
# reproducer.py

import pickle
import requests

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

def test_response_pickleability():
    try:
        response = requests.get('http://example.org')
        pickle.dumps(response)
        # Since we are expecting an error to be thrown before this line, reaching here means the issue is fixed.
        print("NO ERROR: Response object was successfully pickled.")
        exit(0) # Exit with code 0 to indicate the absence of the error.
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("ERROR: Issue when trying to pickle the Response object.")

if __name__ == "__main__":
    test_response_pickleability()
```

This script is meant to reproduce the issue described regarding the pickling of a `Response` object from the `requests` library. It attempts to pickle a response from `http://example.org` and utilizes a custom function `print_stacktrace` to provide clear and detailed stack trace information if an exception is raised during the operation.

The goal of the script is twofold: 
- To assert the presence of the bug through an `AssertionError` if pickling fails. The detailed stack trace of the exception is printed using the `print_stacktrace` function to assist in debugging.
- To automatically exit with code 0 (indicating success) if the issue is resolved and the `Response` object is pickled successfully, which would be a behavior contrary to the expectations set forth by the presence of the issue.

Execution of this script in a Python 3 environment where the requests library is available should replicate the context necessary for identifying and later fixing the pickling issue.