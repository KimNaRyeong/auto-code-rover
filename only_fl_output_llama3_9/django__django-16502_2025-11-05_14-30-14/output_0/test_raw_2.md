Here is the reproducer script:

```python
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import time

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

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def reproduce_issue():
    try:
        server_address = ('127.0.0.1', 8000)
        httpd = HTTPServer(server_address, MyRequestHandler)
        httpd.serve_forever()
        time.sleep(2)  # wait for the server to start
        response = urllib.request.urlopen('http://localhost:8000/', 'HEAD')
        if b'<!DOCTYPE html>' in response.read():
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script starts a simple HTTP server and sends a HEAD request to it. If the response contains HTML content, an AssertionError is raised indicating that the issue is present.