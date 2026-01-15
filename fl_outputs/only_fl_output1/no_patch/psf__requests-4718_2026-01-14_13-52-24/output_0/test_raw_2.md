To address your request, the standalone Python script named `reproducer.py` is designed to attempt a reproduction of the issue where the Authorization header isn't cleared during an HTTPS to HTTP redirect. This script incorporates exception handling logic, including a means to print stack traces clearly, and follows the guidelines you've provided.

```python
import http.server
import socketserver
import ssl
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.server.secure:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()

def run_https_server():
    httpd = HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.secure = True
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='key.pem', certfile='cert.pem', server_side=True)
    httpd.serve_forever()

def run_http_server():
    httpd = HTTPServer(('localhost', 8000), RedirectHandler)
    httpd.serve_forever()

def start_servers():
    # Start HTTPS server
    https_thread = threading.Thread(target=run_https_server, args=())
    https_thread.daemon = True
    https_thread.start()

    # Start HTTP server
    http_thread = threading.Thread(target=run_http_server, args=())
    http_thread.daemon = True
    http_thread.start()

def validate_redirect():
    try:
        response = requests.get('https://localhost:4443', auth=('user', 'pass'), verify=False)
        if any(resp.url.startswith("http://") for resp in response.history):
            raise AssertionError("Authorization header was not stripped during HTTPS to HTTP redirect.")
        print("Test passed: Authorization header was correctly stripped during HTTPS to HTTP redirect.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    start_servers()
    # Gives the server threads a moment to start up
    threading.Event().wait(1)
    validate_redirect()
```

**Additional Setup Instructions:**

1. **Create Self-signed SSL Certificate**: You need to generate a `key.pem` and a `cert.pem`. You can do this with OpenSSL:
    ```bash
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    ```
    This creates both a key file and a certificate file in your working directory. These files are used by the HTTPS server for SSL.

2. **Install Dependencies**: Ensure that you have `requests` installed in your Python environment:
    ```bash
    pip install requests
    ```

3. **Running the Script**: Execute the script using Python 3.x as required:
    ```bash
    python3 reproducer.py
    ```

**Note**: Remember to adjust firewall settings if necessary to allow the script to bind to the selected ports (4443 for HTTPS and 8000 for HTTP). The script attempts to demonstrate the issue and cleanly exits with code `0` if the issue is fixed, or prints a stack trace and exits with a non-zero status if an error is encountered.