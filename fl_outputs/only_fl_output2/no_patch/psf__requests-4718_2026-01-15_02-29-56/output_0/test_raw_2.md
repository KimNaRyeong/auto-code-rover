Based on your request, here is a standalone Python script named `reproducer.py` designed to reproduce the issue of the Authorization header not being cleared during an https -> http redirect. This script sets up both an HTTPS and HTTP server to replicate the scenario. The Authorization header should be stripped when redirecting from https to http to avoid sending credentials over an unencrypted connection.

```python
import http.server
import ssl
import socket
import threading
import requests
from requests.auth import HTTPBasicAuth
import os

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

class RedirectHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()

def https_server_thread():
    httpd = http.server.HTTPServer(('localhost', 4443), RedirectHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.pem', server_side=True)
    httpd.serve_forever()

def http_server_thread():
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(('localhost', 8000), handler)
    httpd.serve_forever()

if __name__ == "__main__":
    # Start HTTPS server
    threading.Thread(target=https_server_thread, daemon=True).start()
    # Start HTTP server
    threading.Thread(target=http_server_thread, daemon=True).start()

    try:
        # Wait for servers to start
        threading.Event().wait(2)

        # Use a session object to persist settings across requests
        session = requests.Session()
        session.verify = False  # Disable SSL cert verification
        session.auth = HTTPBasicAuth('user', 'pass')

        # This header should not be forwarded to HTTP
        captured_headers = []

        def capture_requests(request, *args, **kwargs):
            """Capture request headers"""
            captured_headers.append(request.headers)
            return None

        session.hooks['response'] = [capture_requests]

        # Send HTTPS request and follow redirect to HTTP
        session.get('https://localhost:4443', allow_redirects=True)

        # Check if 'Authorization' header is forwarded
        if any('Authorization' in headers for headers in captured_headers):
            raise AssertionError("Authorization header was not removed on redirect from HTTPS to HTTP")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

    print("Test passed: Authorization header removed on HTTPS to HTTP redirect.")
    exit(0)
```

To run this script:
1. Ensure you have `requests` module installed in your Python environment.
2. You will need a certificate and key combined into `server.pem` for the SSL encryption on the HTTPS server. If you do not have these, you can generate them using OpenSSL with the command:
   ```
   openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
   ```
   Run this in your terminal and follow the prompts to generate `server.pem`.
3. Run the `reproducer.py` script in your project's root directory using Python 3.
4. The script should output "Test passed: Authorization header removed on HTTPS to HTTP redirect." when the issue is fixed, or print a stack trace should the issue persist.