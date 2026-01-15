Certainly! Here is a Python script named `reproducer.py` which attempts to reproduce the issue as described. It sets up an HTTPS server that redirects to an HTTP server. The script then makes an HTTPS request to the first server with authorization, asserting that this authorization should not be forwarded on redirect to HTTP, for security reasons. If the authorization header is forwarded (thereby exposing the credentials in plaintext over HTTP), an `AssertionError` is raised, indicating the presence of the issue.

```python
import http.server
import ssl
import threading
import requests
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

def start_https_server():
    class RedirectHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()

    httpd = http.server.HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                    certfile='yourpemfile.pem', keyfile='yourkeyfile.key')
    httpd.serve_forever()

def start_http_server():
    captured_headers = {}

    class CaptureHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            captured_headers.update(self.headers)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    httpd = http.server.HTTPServer(('localhost', 8000), CaptureHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return captured_headers

def main():
    threading.Thread(target=start_https_server, daemon=True).start()
    captured_headers = start_http_server()

    try:
        requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        assert 'Authorization' not in captured_headers, "Authorization header was forwarded on redirect from HTTPS to HTTP"

    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed. Authorization header not forwarded.")
        exit(0)

if __name__ == '__main__':
    main()
```

Please, make sure to replace `'yourpemfile.pem'` and `'yourkeyfile.key'` in the script with the paths to your certificate and key files, respectively. This script needs an SSL certificate (`yourpemfile.pem`) and a corresponding key (`yourkeyfile.key`) to run the HTTPS server. You can generate self-signed certificates for testing purposes using OpenSSL or another SSL utility.

** Important notes: **
- The HTTP server captures all headers from incoming requests and stores them in `captured_headers`. If the `Authorization` header is present in this dictionary after a request has been redirected from HTTPS to HTTP, the script considers the test failed, thus reproducing the issue.
- This script uses the standard `http.server` module available in Python 3; make sure you run it with a Python 3 interpreter (modify the execution command accordingly if necessary).
- You have to set up SSL certificates (`yourpemfile.pem` and `yourkeyfile.key`) for the HTTPS server to start properly. For a real-world scenario or testing environment where security concerns are higher, use proper certificates issued by a trusted Certificate Authority (CA).