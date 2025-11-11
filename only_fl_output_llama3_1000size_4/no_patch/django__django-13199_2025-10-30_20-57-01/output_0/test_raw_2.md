Here is the reproducer script:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import traceback
import sys

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        class TestRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Hello, world!')

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_body = self.rfile.read(content_length).decode('utf-8')
                query_params = urllib.parse.parse_qs(post_body)
                if 'messages' in query_params:
                    self.send_response(304)
                    self.send_header('Set-Cookie', 'messages=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
                    self.end_headers()
                else:
                    self.send_response(200)

        httpd = HTTPServer(('localhost', 8000), TestRequestHandler)
        httpd.serve_forever()
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present")
        exit(0)

if __name__ == '__main__':
    main()
```

This script creates a simple HTTP server that responds to GET and POST requests. When the POST request contains a 'messages' parameter, it sets a cookie with SameSite set to Lax. Then, when the same request is made again (which should delete the cookie), the HttpResponse.delete_cookie() method does not preserve the SameSite attribute, resulting in a warning message from Firefox.

To run this script, save it as `reproducer.py` and execute it using `python3 reproducer.py`.