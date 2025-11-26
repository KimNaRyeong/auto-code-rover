I apologize for the previous mistake. Here is a new standalone Python script `reproducer.py` to reproduce the issue:
```python
import requests
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write('')

def run_https_server():
    httpd = HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                  certfile='yourpemfile.pem')
    httpd.serve_forever()

def run_http_server():
    def handler(*args):
        return "HTTP Server"
    httpd = HTTPServer(('localhost', 8000), handler)
    httpd.serve_forever()

def test_redirect():
    try:
        t1 = threading.Thread(target=run_https_server)
        t2 = threading.Thread(target=run_http_server)
        t1.start()
        t2.start()

        response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)

        # Check if the Authorization header is sent in plaintext
        request_headers = response.request.headers
        assert 'Authorization' not in request_headers, "Authorization header was not stripped"

    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    test_redirect()
```
This script sets up an HTTPS server on `localhost:4443` that redirects to `http://localhost:8000`, and a plain HTTP server on `localhost:8000`. It then sends a request to the HTTPS server with basic auth credentials, and checks if the Authorization header is sent in plaintext to the HTTP server. If it is, an `AssertionError` is raised.

Please replace `'yourpemfile.pem'` with the path to your SSL certificate file.