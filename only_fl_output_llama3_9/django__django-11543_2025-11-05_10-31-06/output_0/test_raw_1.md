Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote
import time
import random
import select

class ReproducerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def run_server():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, ReproducerRequestHandler)
    print("Starting WSGI server...")
    httpd.serve_forever()

def main():
    try:
        os.environ['WsgiRequestTimeout'] = '1'
        threading.Thread(target=run_server).start()
        for _ in range(100):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 8000))
            s.send(b'GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: keep-alive\r\n\r\n')
            data = s.recv(1024)
            if not data:
                raise AssertionError("Server did not respond")
        time.sleep(10)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()

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

```

This script starts a simple HTTP server using the `http.server` module. The server listens on port 8000 and responds to GET requests with "Hello, World!".

To reproduce the issue, run this script and then use a web browser (like Chrome or Firefox) to make multiple GET requests to `http://localhost:8000/`. You should see that the server stops responding after some time.