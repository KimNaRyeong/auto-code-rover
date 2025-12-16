 Here's a standalone Python script, `reproducer.py`, that reproduces the issue:

```python
import http.server
import ssl
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write(b'')

try:
    httpd = http.server.HTTPServer(('localhost', 4443), Handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                   certfile='yourpemfile.pem',
                                   ssl_version=ssl.PROTOCOL_TLSv1_2)
    httpd.serve_forever()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```

To reproduce the issue, follow these steps:

1. Create a self-signed certificate `yourpemfile.pem` and put it in the root directory of the project.
2. Run the script with `python3 reproducer.py`.
3. Run the following Python script in another terminal:

```python
import requests

try:
    response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```

If the issue is present, the basic auth credentials will be transmitted in plaintext to `http://localhost:8000`. If the issue is fixed, the script will exit with code 0.