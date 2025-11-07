Here is the corrected `reproducer.py` file that reproduces the issue:
```
import os
from django.http.multipartparser import MultiPartParser
from io import BytesIO
from django.core.files.uploadhandler import TemporaryFileUploadHandler

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
    parser = MultiPartParser(BytesIO(request_body), 'multipart/form-data; boundary=----------------------------677822685948106391633425', upload_handlers=[TemporaryFileUploadHandler()])
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
This script should correctly reproduce the issue. The `MultiPartParser` constructor was missing the required `upload_handlers` argument, which is now provided.