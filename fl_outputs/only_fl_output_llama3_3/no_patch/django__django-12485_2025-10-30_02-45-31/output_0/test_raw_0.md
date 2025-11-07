Here is the reproducer script `reproducer.py`:

```python
import requests
from django.http.multipartparser import MultiPartParser
from django.core.files.uploadhandler import FakeFileUploadHandler
from django.utils.encoding import force_text

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
    data = {
        'file': ('测试.txt", text/plain; filename="测试.txt"; filename*="UTF-8''%E6%B5%8B%E8%AF%95.txt"',
                 b'test')
    }
    parser = MultiPartParser(FakeFileUploadHandler())
    request = requests.Request('POST', 'http://example.com', data=data)
    response = parser.parse_request(request)

    if force_text(response['file'].name) != "测试.txt":
        raise AssertionError("Expected filename to be '测试.txt' but got '{}'".format(force_text(response['file'].name)))

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sends a POST request with the given data and checks if the parsed filename is "测试.txt" or not. If it's not, an `AssertionError` is raised, which will be caught by the script and printed along with its stack trace.