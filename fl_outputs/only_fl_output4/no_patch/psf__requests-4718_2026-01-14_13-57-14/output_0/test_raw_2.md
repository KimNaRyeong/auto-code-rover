To address the previous confusion and align with your request, let's craft a `reproducer.py` that aims to reproduce the issue detailed in the initial problem statement efficiently. This script will attempt to intercept the Authorization header's presence in a redirected HTTP request after an initial HTTPS request. This scenario simulates a real-world issue where sensitive data could leak in plain text due to an HTTPS to HTTP redirection. Below is the standalone Python script:

```python
import http.server
import ssl
import threading
import requests
import socket
from urllib.parse import urlparse

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

class HTTPRedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()

def http_redirect_server():
    httpd = http.server.HTTPServer(('localhost', 4443), HTTPRedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.pem', server_side=True)
    httpd.serve_forever()

class HTTPCaptureHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global captured_headers
        captured_headers = self.headers
        self.send_response(200)
        self.end_headers()

def http_capture_server():
    httpd = http.server.HTTPServer(('localhost', 8000), HTTPCaptureHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    captured_headers = None

    # The server.pem file needs to exist in the same directory as this script.
    # You can generate one using OpenSSL with the following command:
    # openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

    # Starting HTTPS redirect server
    thread_https = threading.Thread(target=http_redirect_server, daemon=True)
    thread_https.start()

    # Starting HTTP capture server
    thread_http = threading.Thread(target=http_capture_server, daemon=True)
    thread_http.start()

    try:
        # This is a makeshift way to allow the servers to start up.
        import time
        time.sleep(2)

        # Making the HTTPS request that will be redirected to HTTP
        requests.get('https://localhost:4443', auth=('user', 'pass'), verify=False)

        # Checking if the Authorization header was carried over to the redirected HTTP request
        assert captured_headers is not None, "The HTTP request was not captured."
        authorization_header = captured_headers.get('Authorization')
        assert authorization_header is None, "Authorization header should not be present in the HTTP redirected request."

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(2)

    print("No security issue detected; the Authorization header was not leaked.")
    sys.exit(0)
```

Please note the comments within the code, especially regarding the `server.pem` file required for the HTTPS server. This script is designed to exit with code 0 when the issue is fixed, meaning it confirms that the `Authorization` header is not leaked upon redirection from HTTPS to HTTP. Conversely, if the issue is present and the `Authorization` header is leaked, an `AssertionError` is raised, and a detailed stack trace is printed to `stderr`.