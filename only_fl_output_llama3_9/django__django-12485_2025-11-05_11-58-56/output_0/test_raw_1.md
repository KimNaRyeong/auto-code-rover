Here is the reproducer script:

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
    body = 'test'

    try:
        _, data = parse_header(headers['Content-Disposition'])
        file_name = data.get('filename', '').strip('"')
        assert file_name == "测试.txt", f"Expected '测试.txt' but got '{file_name}'"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script uses Django's `MultiPartParser` and `parse_header` functions to parse the given headers. It then checks if the file name is correctly parsed. If not, it prints the stack trace of the assertion error and exits with code 1.