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

def delete_cookie(self, key, path='/', domain=None):
    self.set_cookie(key, max_age=0, path=path, expires='Thu, 01 Jan 1970 00:00:00 GMT', domain=domain if domain is not None else 'example.com', secure=False, httponly=True, samesite='Lax')

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Set-Cookie', 'messages=; HttpOnly; Path=/; SameSite=Lax')
        self.end_headers()

    def do_POST(self):
        if parse_qs(urlparse(self.path).query)['delete'] == ['1']:
            self.send_response(304)
            self.send_header('Set-Cookie', 'messages=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Set-Cookie', 'messages=(... encoded message text ...); HttpOnly; Path=/; SameSite=Lax')
            self.end_headers()

def main():
    port = 8000
    server_address = ('localhost', port)

    httpd = http.server.HTTPServer(server_address, TestRequestHandler)
    print(f"Starting server on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    if not parse_qs(urlparse('http://localhost:8000/delete').query)['delete'] == ['1']:
        raise AssertionError("Issue present")
    else:
        print_stacktrace(Exception("Issue fixed"))
        exit(0)

if __name__ == "__main__":
    main()
```

This script reproduces the issue by using `HttpResponseBase's delete_cookie method` to expire a cookie without preserving its SameSite attribute.