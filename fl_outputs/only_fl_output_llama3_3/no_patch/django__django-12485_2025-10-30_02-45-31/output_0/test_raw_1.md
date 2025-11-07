Here is the reproducer script `reproducer.py`:

```python
import requests
from django.http.multipartparser import MultiPartParser
from io import BytesIO
from urllib.parse import urlparse, parse_qs

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
    data = BytesIO()
    data.write(b'Content-Disposition: form-data; name="file"; filename="测试.txt"; filename*="UTF-8''%E6%B5%8B%E8%AF%95.txt"\r\n')
    data.write(b'Content-Type: text/plain\r\n\r\n')
    data.write(b'test')

    parser = MultiPartParser()
    request = requests.Request('POST', 'http://example.com', data=data.getvalue().decode('utf-8'))
    response = parser.parse_request(request)

    parsed_qs = parse_qs(urlparse(response['Content-Disposition']).query)
    if force_text(parsed_qs.get('filename')[0]) != "测试.txt":
        raise AssertionError("Expected filename to be '测试.txt' but got '{}'".format(force_text(parsed_qs.get('filename')[0])))

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sends a POST request with the given data and checks if the parsed filename is "测试.txt" or not. If it's not, an `AssertionError` is raised, which will be caught by the script and printed along with its stack trace.