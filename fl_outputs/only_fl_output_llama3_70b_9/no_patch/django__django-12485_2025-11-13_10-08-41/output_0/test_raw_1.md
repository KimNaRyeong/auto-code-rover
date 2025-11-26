I apologize for the previous mistake. Here is a new `reproducer.py` file that should reproduce the issue:
```
import os
from django.http.multipartparser import MultiPartParser
from io import BytesIO
from django.core.handlers.wsgi import WSGIRequest

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
    environ = {
        'REQUEST_METHOD': 'POST',
        'CONTENT_TYPE': 'multipart/form-data; boundary=----------------------------677822685948106391633425',
        'wsgi.input': BytesIO(request_body),
    }
    request = WSGIRequest(environ)
    try:
        parsed_data = MultiPartParser(request.META, request.FILES).parse()
        filename = parsed_data[0][2]['filename']
        assert filename == '\xe6\xb5\x8b\xe8\xaf\x95.txt', f"Expected filename to be '\xe6\xb5\x8b\xe8\xaf\x95.txt' but got '{filename}'"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    reproduce_issue()
```
This script creates a WSGI request with the multipart/form-data body and then parses it using Django's `MultiPartParser`. It checks if the parsed filename matches the expected value. If not, it raises an `AssertionError` with a stack trace.

Please save this file as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.