Here is the reproducer script in a code block:

```python
import http.server
from urllib.parse import urlparse, parse_qs

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if 'messages' not in self.headers:
            self.send_response(200)
            self.send_header('Set-Cookie', 'messages=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
            self.end_headers()
        else:
            self.send_response(304)

    def do_POST(self):
        if 'messages' not in parse_qs(urlparse(self.path).query):
            self.send_response(200)
            self.send_header('Set-Cookie', 'messages=some_value; HttpOnly; Path=/; SameSite=Lax')
            self.end_headers()
        else:
            self.send_response(304)

def main():
    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print("Starting server...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print_stacktrace(Exception("Test failed"))

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

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

This script creates a simple HTTP server that responds to GET and POST requests. The server sets the 'messages' cookie in the response headers, but when it receives a request with the 'messages' query parameter, it returns a 304 status code and sets an empty cookie with SameSite set to Lax.