To create a reproducer for this issue, we'll need a script (`reproducer.py`) that accomplishes a few things:
1. Starts an HTTPS server that redirects to an HTTP endpoint.
2. Makes a request to this server with Authorization credentials.
3. Checks whether these credentials are sent over plain HTTP after the redirect.
4. Asserts an error if the credentials are indeed sent over plain HTTP.

Let's create `reproducer.py`:

```python
import threading
import socket
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# Function to print stacktrace
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

# Handler for HTTPS server that redirects to HTTP
class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()

# Simple HTTP server to catch the redirect
class CatchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_headers
        captured_headers = self.headers
        self.send_response(200)
        self.end_headers()

def run_https_server():
    httpd = HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='yourpemfile.pem')
    httpd.serve_forever()

def run_http_server():
    httpd = HTTPServer(('localhost', 8000), CatchHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    # Start the redirecting HTTPS server
    https_thread = threading.Thread(target=run_https_server, daemon=True)
    https_thread.start()

    # Start the catching HTTP server
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Make an HTTPS request that will be redirected to HTTP
    try:
        requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        global captured_headers
        assert 'Authorization' not in captured_headers, "Authorization header should not be present in redirected request"
        print("No Authorization header leaked. Issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
```

Please note, this script includes a few key considerations:
- You need to replace `'yourpemfile.pem'` with the path to a valid PEM file for the HTTPS server. This file includes the certificate and private key.
- The script uses global variables (`captured_headers`) and threads (`https_thread` and `http_thread`) to simplify the demonstration, but these patterns may not be best practice for production code.
- The script doesn't use an explicit wait/check to ensure the servers are ready before sending requests. In a more robust solution, you might want to add such synchronization.
- The usage of `daemon=True` in thread creation ensures that the threads will not prevent the script from exiting.
- Security warnings (from `verify=False`) and potential issues with using a hardcoded port (if the port is already in use) are not handled in this script.

Remember, this script is meant to be executed in an environment where it's safe to run both HTTP and HTTPS servers, and there's no conflict with the chosen ports. Also, ensure you have the `requests` module installed in your Python environment.