Here is the `reproducer.py` file that reproduces the issue:
```
import os
from urllib.parse import urlparse, parse_qs
from django.http.multipartparser import MultiPartParser

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
    parser = MultiPartParser(request_body, 'multipart/form-data; boundary=----------------------------677822685948106391633425')
    data = {}
    for part in parser.parts():
        disposition = part.disposition_options
        if 'filename' in disposition:
            filename = disposition['filename']
            assert filename == '\xe6\xb5\x8b\xe8\xaf\x95.txt', f"Expected filename to be '\xe6\xb5\x8b\xe8\xaf\x95.txt', but got {filename}"
    print("Issue not present")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script uses the `MultiPartParser` from Django to parse a request body with a filename wrapped in double quotes. It then asserts that the parsed filename is correct, and if not, it raises an `AssertionError`. The `print_stacktrace` function is used to print a stack trace of the error.

You can run this script using `python3 reproducer.py`, and it should raise an `AssertionError` with a stack trace when the issue is present. If the issue is fixed, the script will exit with code 0.