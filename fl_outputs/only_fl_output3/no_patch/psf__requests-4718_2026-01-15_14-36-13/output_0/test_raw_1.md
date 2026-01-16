Certainly! To address the requirement fully, let's craft a standalone Python script named `reproducer.py` to reproduce the issue under discussion. This script encapsulates the functionality to:

1. Start an HTTPS server which, upon receiving a GET request, responds with a 302 redirect to an HTTP URL.
2. Start an HTTP server to capture the redirected request and examine its headers for the presence of the `Authorization` header.
3. Make an initial HTTPS request with basic authentication to demonstrate whether the `Authorization` header gets stripped or not after redirection from HTTPS to HTTP.

This script intends to automate the testing process thoroughly and prints a detailed stack trace if an error occurs. Moreover, it exits with code 0 if the issue concerning the `Authorization` header is resolved (i.e., the header is appropriately stripped during the redirect from HTTPS to HTTP).

```python
import threading
import http.server
import ssl
import requests
import traceback
import sys
from socketserver import TCPServer


def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()


class CaptureHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global captured_headers
        captured_headers = self.headers
        self.send_response(200)
        self.end_headers()


def start_https_server(server_class=TCPServer, handler_class=RedirectHandler, port=4443, certfile='cert.pem'):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, server_side=True)
    httpd.serve_forever()


def start_http_server(server_class=TCPServer, handler_class=CaptureHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    captured_headers = None

    https_thread = threading.Thread(target=start_https_server)
    https_thread.daemon = True
    https_thread.start()

    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    try:
        response = requests.get('https://localhost:4443', auth=('user', 'pass'), verify=False)
        
        # Ensuring that the server had enough time to process and log the headers
        threading.Event().wait(1)

        assert captured_headers is not None, "No headers captured; possible issue with HTTP server setup."
        assert 'Authorization' not in captured_headers, "Authorization header leaked in redirect from HTTPS to HTTP."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Test passed. No Authorization header leaked.")
    sys.exit(0)
```

Please make sure you have a self-signed SSL certificate named `cert.pem` in your project root directory for the HTTPS server. If you don't have a certificate, you can generate one using OpenSSL with the following command:

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

And you should combine the generated `key.pem` with `cert.pem` for the script to use if required. 

The script uses threads to run both servers simultaneously, ensuring they operate in the background while the main thread makes the request and verifies the result. It should help you reproduce the issue effectively under the described conditions.