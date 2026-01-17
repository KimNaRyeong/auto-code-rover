```python
# reproducer.py
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

def run_ssl_server():
    class RedirectHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()

    httpd = HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='key.pem', certfile='cert.pem', server_side=True)
    httpd.serve_forever()

def run_http_server():
    class CaptureHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            global captured
            captured = self.headers.get('Authorization')
            self.send_response(200)
            self.end_headers()
    
    httpd = HTTPServer(('localhost', 8000), CaptureHandler)
    httpd.serve_forever()

def start_servers():
    threading.Thread(target=run_ssl_server, daemon=True).start()
    threading.Thread(target=run_http_server, daemon=True).start()

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
    start_servers()
    
    captured = None
    try:
        # Wait a moment for the servers to start
        import time
        time.sleep(2)  

        requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        
        if captured is not None:
            raise AssertionError("Authorization header was not stripped in http redirect.")
        else:
            print("No Authorization header captured. Issue is not present.")
    except Exception as e:
        print_stacktrace(e)
```

This script starts both an HTTPS and an HTTP server on localhost, with the former redirecting to the latter. It then sends a request with basic authentication to the HTTPS server and checks if the `Authorization` header is captured by the HTTP server after redirection, which would demonstrate that sensitive information was sent in plaintext.

Note: Before running this script, it's necessary to have a `key.pem` and a `cert.pem` file in the current directory for the SSL encryption. These can be created with OpenSSL or other similar tools. Also, keep in mind the global variable 'captured' for capturing the `Authorization` header might not work as expected in a multi-threaded environment due to race conditions, but for the simplicity of this script and its purpose (single request check), it should suffice.