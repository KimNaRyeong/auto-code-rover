Here is the reproducer script:

```python
import http.server
from urllib.parse import parse_qs, urlparse
from io import BytesIO
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
    request = http.server.BaseHTTPRequestHandler()
    request.path = "/upload"
    request.body = BytesIO(b"Content-Disposition: form-data; name=\"file\"; filename=\"测试.txt\"; filename*=UTF-8''%E6%B5%8B%E8%AF%95.txt\r\nContent-Type: text/plain\ntest\r\n--")
    request.headers["Content-Length"] = str(len(request.body.getvalue()))
    request.headers["Content-Type"] = "multipart/form-data"
    
    query_string = urlparse("http://example.com/upload", scheme="http").query
    query_dict = QueryDict(query_string)
    request.GET = query_dict
    
    try:
        from django.http.request import HttpRequest
        from django.utils.encoding import force_text
        
        request = HttpRequest()
        request.META["CONTENT_TYPE"] = "multipart/form-data"
        request.META["HTTP_CONTENT_LENGTH"] = str(len(request.body.getvalue()))
        
        filename = request.POST.get("file")
        assert force_text(filename) == "测试.txt", f"Expected '测试.txt' but got {force_text(filename)}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a fake HTTP request with the given content and then attempts to parse the filename from the request. If the filename is not correctly parsed, it prints the stack trace and exits with code 1.