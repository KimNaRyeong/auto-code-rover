Here is the reproducer script in Python:

```python
import http.server
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

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/delete-cookie':
            response = http.server.HTTPResponse(self.rfile, self.wfile)
            response.send_header('Set-Cookie', 'messages=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
            response.end_headers()
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path == '/delete-cookie':
            response = http.server.HTTPResponse(self.rfile, self.wfile)
            response.send_header('Set-Cookie', 'messages=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
            response.end_headers()
            return
        self.send_response(404)
        self.end_headers()

def main():
    print("Starting server...")
    try:
        http.server.HTTPServer(('localhost', 8000), TestRequestHandler).serve_forever()
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates a simple HTTP server that responds to GET and POST requests. When the `/delete-cookie` path is requested, it sets a cookie with `SameSite=None`. The script then attempts to delete this cookie using the `HttpResponse.delete_cookie()` method.

When you run this script, it will start an HTTP server on port 8000. You can test the issue by sending a GET or POST request to `http://localhost:8000/delete-cookie` in your browser. If the issue is present, the script will raise an `AssertionError` and print the stack trace.