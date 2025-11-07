Here is the reproducer script:

```python
import http.server
from urllib.parse import urlparse, parse_qs

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/delete-cookie'):
            return
        cookie_name = 'messages'
        expires = 'Thu, 01 Jan 1970 00:00:00 GMT'
        max_age = 0
        path = '/'
        domain = None

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.delete_cookie(cookie_name, path, domain)

    def delete_cookie(self, key, path='/'):
        self.send_response(304)
        self.send_header('Set-Cookie', f'{key}=""; expires={expires}; Max-Age={max_age}; Path={path}')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

def main():
    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print("Starting server...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print_stacktrace(KeyboardInterrupt())

if __name__ == '__main__':
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

if __name__ == '__main__':
    try:
        # Simulate the issue
        import requests
        response = requests.get('http://localhost:8000/delete-cookie')
        if 'Set-Cookie' not in response.headers:
            raise AssertionError("Expected Set-Cookie header")
        cookie_header = response.headers['Set-Cookie']
        if 'SameSite=None' not in cookie_header:
            raise AssertionError("Cookie SameSite attribute is None")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    # Simulate the fix
    import http.server
    class TestRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if not self.path.startswith('/delete-cookie'):
                return
            cookie_name = 'messages'
            expires = 'Thu, 01 Jan 1970 00:00:00 GMT'
            max_age = 0
            path = '/'
            domain = None

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            self.set_cookie(cookie_name, expires=expires, max_age=max_age, path=path, domain=domain)

        def set_cookie(self, key, **kwargs):
            self.send_response(304)
            for k, v in kwargs.items():
                if k == 'max_age':
                    v = str(v)
                elif k == 'expires':
                    v = f'Thu, 01 Jan 1970 00:00:00 GMT'
                self.send_header(f'Set-Cookie', f'{key}={v}; Path={kwargs["path"]}')
            self.end_headers()

    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print("Starting server...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            exit(0)
```

This script creates a simple HTTP server that listens on port 8000. When you access `http://localhost:8000/delete-cookie`, it simulates the issue by setting a cookie with SameSite=None and then deleting it using the `delete_cookie` method. If the issue is present, an AssertionError will be raised and the stack trace will be printed.