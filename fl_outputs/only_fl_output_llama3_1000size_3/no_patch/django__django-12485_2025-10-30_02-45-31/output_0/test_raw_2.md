I apologize for the previous mistake. Here is a new reproducer script `reproducer.py`:

```python
import requests
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
    data.write(b'Content-Disposition: form-data; name="file"; filename="测试.txt"; filename*="%E6%B5%8B%E8%AF%95.txt"\r\n')
    data.write(b'Content-Type: text/plain\r\n\r\n')
    data.write(b'test')

    request = requests.Request('POST', 'http://example.com', files={'file': data.getvalue()})
    response = request.prepare()

    parsed_qs = parse_qs(urlparse(response.headers['Content-Disposition']).query)
    if force_text(parsed_qs.get('filename')[0]) != "测试.txt":
        raise AssertionError("Expected filename to be '测试.txt' but got '{}'".format(force_text(parsed_qs.get('filename')[0])))

def force_text(s):
    return s.decode('utf-8')

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sends a POST request with the given data and checks if the parsed filename is "测试.txt" or not. If it's not, an `AssertionError` is raised, which will be caught by the script and printed along with its stack trace.