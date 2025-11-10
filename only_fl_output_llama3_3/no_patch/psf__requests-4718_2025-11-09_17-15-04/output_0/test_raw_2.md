Here is the reproducer script in Python:

```python
import requests
import BaseHTTPServer
import ssl
import sys

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
        response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False, allow_redirects=True)
        if response.status_code == 200:
            raise AssertionError("Expected a redirect")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), Handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                    certfile='yourpemfile.pem')
    httpd.serve_forever()
    reproduce_issue()

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write('')
```

This script sets up an HTTPS server on `localhost:4443` that redirects requests to `http://localhost:8000`. It then makes a GET request to the HTTPS endpoint with basic authentication and checks if the response is a redirect. If it's not, it raises an assertion error and prints the stack trace.

Note that you'll need to replace `'yourpemfile.pem'` with the path to your SSL certificate file.

This script should be executed by `python3 reproducer.py`.