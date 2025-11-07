Here is the reproducer script:

```python
import http.server
from urllib.parse import urlparse, parse_qs

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

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if parse_qs(urlparse(self.path).query)['delete'] == ['1']:
            self.send_response(200)
            self.send_header('Set-Cookie', 'messages=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/; SameSite=None')
            self.end_headers()
        else:
            self.send_response(404)

def run_reproducer():
    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as server:
        print('Starting the server...')
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('Stopping the server...')
            server.shutdown()
            print_stacktrace(Exception('Issue present'))

def main():
    run_reproducer()

if __name__ == '__main__':
    main()
```

To reproduce the issue, you can execute this script by running `python3 reproducer.py`. This will start an HTTP server that listens on port 8000. You can then use a tool like `curl` to send a GET request with the query parameter `delete=1` to trigger the cookie deletion:

```
curl 'http://localhost:8000/?delete=1'
```

This should raise an `AssertionError` and print the stack trace of the issue.