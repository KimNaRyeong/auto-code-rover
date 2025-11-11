Here is the reproducer script in Python:

```python
import requests
import BaseHTTPServer
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

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
    try:
        requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present")

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 4443), MyHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                    certfile='yourpemfile.pem')
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write('')
```

This script sets up an HTTPS server on port 4443 that redirects requests to `http://localhost:8000`. It then sends a GET request with basic authentication to the HTTPS endpoint. If the issue is present, it will print the stack trace and raise an `AssertionError` with code 1.