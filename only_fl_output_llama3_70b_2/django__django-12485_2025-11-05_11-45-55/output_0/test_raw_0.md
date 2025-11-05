Here is the `reproducer.py` file that reproduces the issue:
```
import os
from django.http.multipartparser import MultiPartParser
from io import BytesIO

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

def reproduce_issue():
    request_body = b'''
----------------------------677822685948106391633425
Content-Disposition: form-data; name="file"; filename="\xe6\xb5\x8b\xe8\xaf\x95.txt"; filename*="UTF-8''%E6%B5%8B%E8%AF%95.txt"
Content-Type: text/plain

test
----------------------------677822685948106391633425--
'''
    parser = MultiPartParser(BytesIO(request_body), 'multipart/form-data; boundary=----------------------------677822685948106391633425')
    data = {}
    for part in parser.parse():
        if part.name == 'file':
            filename = part.disposition_params['filename']
            assert filename == '\xe6\xb5\x8b\xe8\xaf\x95.txt', f"Expected filename to be '\xe6\xb5\x8b\xe8\xaf\x95.txt' but got {filename}"
    print("Issue not present, exiting with code 0")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script sends a multipart request to Django's `MultiPartParser` and checks if the filename is correctly parsed. If the issue is present, it raises an `AssertionError` with a message indicating that the filename was not correctly parsed. The `print_stacktrace` function is used to print the stack trace of the error.

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and exit with code 1. If the issue is fixed, it will print "Issue not present, exiting with code 0" and exit with code 0.