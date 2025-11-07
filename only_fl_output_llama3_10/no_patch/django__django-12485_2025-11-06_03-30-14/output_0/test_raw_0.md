Here is the reproducer script:

```python
import http.server
from urllib.parse import parse_qs, urlparse
from io import StringIO
from django.http.request import QueryDict
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
    request_data = b"""
Content-Disposition: form-data; name="file"; filename="测试.txt"; filename*="UTF-8''%E6%B5%8B%E8%AF%95.txt"
Content-Type: text/plain

test
"""

    req = http.server.BaseHTTPRequestHandler()
    req.RANGE = "bytes=0-9"

    query_string = b"foo=bar&baz=qux"
    parsed_qs = parse_qs(query_string.decode("utf-8"))
    query_dict = QueryDict(query_string.decode("utf-8"))

    request_uri = "/test"
    parsed_url = urlparse(request_uri)
    req.path_info = parsed_url.path
    req.query_string = query_string

    req.rfile = StringIO(request_data.decode("utf-8"))
    req.raw_requestline = "POST /test HTTP/1.0"

    try:
        req.parse_request()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script simulates a POST request with the given Content-Disposition and filename, then attempts to parse it using Django's `http.request.Request` class. If an exception is raised during parsing, it prints the stack trace and raises an AssertionError.