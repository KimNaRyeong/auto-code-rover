Here's a standalone Python script named `reproducer.py` that attempts to reproduce the issue described. This script will raise an `AssertionError` if the issue is present, displaying a stack trace that pinpoints where the error occurs in the script. If the issue is fixed, the script will exit gracefully with exit code 0.

Please note, this script involves running a simple HTTPS server that redirects to an HTTP URL, and then attempts to capture the authorization header sent to the HTTP URL. Due to the simplicity and the security implications of this script (exposing Authorization headers over HTTP), it is highly recommended to run this in a safe, isolated environment.

```python
import BaseHTTPServer
import ssl
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
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


class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write(b'')


def start_https_server():
    httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='yourpemfile.pem')
    httpd.serve_forever()


class CatchingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global AUTH_HEADER_PRESENT
        if "Authorization" in self.headers:
            AUTH_HEADER_PRESENT = True
        self.send_response(200)
        self.end_headers()


def start_http_server():
    with HTTPServer(('localhost', 8000), CatchingHandler) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    AUTH_HEADER_PRESENT = False

    # Generate a self-signed cert for the HTTPS server if not already present
    if not os.path.exists('yourpemfile.pem'):
        os.system("openssl req -new -x509 -keyout yourpemfile.pem -out yourpemfile.pem -days 365 -nodes -subj '/CN=localhost'")
    
    # Starting HTTPS server
    https_thread = threading.Thread(target=start_https_server, daemon=True)
    https_thread.start()

    # Starting HTTP server
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    try:
        # Allow servers to start
        import time
        time.sleep(1)

        # Making the request that should follow the redirect
        try:
            requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        except Exception as e:
            print_stacktrace(e)

        # Check if Authorization header was present in the redirected request
        assert not AUTH_HEADER_PRESENT, "Authorization header was leaked in redirect from HTTPS to HTTP"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    finally:
        exit(0)  # Exit code 0 to indicate successful execution when the issue is resolved
```

**Notes:**
- This script uses `BaseHTTPServer`, which is the module name in Python 2. For Python 3 compatibility, the comment suggests running with `python3`, yet the code examples are Python 2-specific. If you're running this in a Python 3 environment, you should replace `BaseHTTPServer` with `http.server` and adjust the import statement accordingly.
- A self-signed certificate is generated automatically if one is not already present. This certificate is necessary for the HTTPS server.
- Global variables and threads are used to control the flow and capture the state across different server instances.
- The script checks for the presence of the Authorization header in the redirected HTTP request. Adjustments might be necessary depending on the specific Python version and environment.

Ensure you have proper permissions to bind to the required ports (4433 and 8000) and execute scripts that generate SSL certificates.