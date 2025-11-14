Here is the reproducer script:

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

def main():
    class TestRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if not self.path.startswith('/delete-cookie'):
                return
            cookie_name = 'messages'
            expires = 'Thu, 01 Jan 1970 00:00:00 GMT'
            max_age = 0
            path = '/'
            domain = None

            self.send_response(304)
            self.send_header('Set-Cookie', f'{cookie_name}=""; expires={expires}; Max-Age={max_age}; Path={path}')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

        def do_POST(self):
            if not self.path.startswith('/messages'):
                return
            cookie_name = 'messages'
            value = 'encoded message text'
            expires = 'Thu, 01 Jan 1970 00:00:00 GMT'
            max_age = 0
            path = '/'
            domain = None

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            self.send_response(200)
            self.send_header('Set-Cookie', f'{cookie_name}={value}; expires={expires}; Max-Age={max_age}; Path={path}; SameSite=Lax')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print("Starting server...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            if not hasattr(self, '_Thread__stop'):
                raise AssertionError("Expected SameSite attribute to be None")
            exit(1)

    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print("Starting server...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            if hasattr(self, '_Thread__stop'):
                raise AssertionError("Expected SameSite attribute to be Lax")
            exit(0)

if __name__ == '__main__':
    main()
```

This script creates a simple HTTP server that listens on port 8000. When you access `http://localhost:8000/delete-cookie`, it simulates the issue by setting a cookie with SameSite=None and then deleting it using the `delete_cookie` method. If the issue is present, an AssertionError will be raised and the stack trace will be printed.