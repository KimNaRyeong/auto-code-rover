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
    print("Issue is fixed!")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

reproduce_issue()
```
This script sends a multipart request with a filename wrapped in double quotes, similar to the Postman request body provided. It then uses Django's `MultiPartParser` to parse the request and extracts the filename from the parsed data. The script asserts that the extracted filename matches the expected value without double quotes. If the assertion fails, it prints a stack trace of the issue using the provided `print_stacktrace` function and exits with code 1. If the issue is fixed, the script prints "Issue is fixed!" and exits with code 0.