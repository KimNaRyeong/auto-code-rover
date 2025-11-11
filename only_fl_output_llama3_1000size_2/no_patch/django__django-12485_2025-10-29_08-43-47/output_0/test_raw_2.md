I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
import requests
from django.http.multipartparser import MultiPartParser, parse_header

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
    headers = {
        'Content-Disposition': 'form-data; name="file"; filename="测试.txt"; filename*="UTF-8''%E6%B5%8B%E8%AF%95.txt"',
        'Content-Type': 'text/plain'
    }
    try:
        parser = MultiPartParser()
        _, value = parse_header(headers['Content-Disposition'].encode('utf-8'))
        assert value == "测试.txt"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a `MultiPartParser` and uses the `parse_header` function to parse the given headers. It then checks if the parsed filename is equal to "测试.txt". If it's not, an `AssertionError` is raised and the stack trace is printed.