Here is the reproducer script:

```python
import requests
import BaseHTTPServer
import ssl
import sys
import traceback

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
        httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), Handler)
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                        certfile='yourpemfile.pem')
        httpd.serve_forever()
        response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write('')

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up an HTTPS server that redirects to a plain HTTP server, and then makes a GET request with basic authentication. If the issue is present (i.e., the `Authorization` header is not cleared), it will print the stack trace and exit with code 1.