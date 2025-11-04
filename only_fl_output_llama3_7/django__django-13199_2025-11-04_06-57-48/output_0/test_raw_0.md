Here is the reproducer script:

```python
import http.server
from urllib.parse import urlparse, parse_qs

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if 'messages' in self.headers:
            self.send_response(304)
            self.delete_cookie('messages')
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    def delete_cookie(self, key):
        self.send_response(200)
        self.send_header("Set-Cookie", f"{key}=''; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/")
        self.end_headers()

def main():
    with http.server.HTTPServer(("", 8000), TestRequestHandler) as httpd:
        print("Serving HTTP on port 8000...")
        try:
            while True:
                httpd.handle_request()
        except KeyboardInterrupt:
            pass
    print_stacktrace(AssertionError("Issue not reproduced"))

if __name__ == "__main__":
    main()

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

```

This script starts an HTTP server that listens on port 8000. When a GET request is made to the server, it checks if there's a 'messages' cookie in the request headers. If there is, it sends a 304 response and deletes the cookie using the `delete_cookie` method.