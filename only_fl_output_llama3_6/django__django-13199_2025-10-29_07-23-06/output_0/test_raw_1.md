Here is the reproducer script:

```python
import http.server
from urllib.parse import urlparse, parse_qs

class TestRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_post_data = parse_qs(urlparse(post_data).query)
        if 'messages' in parsed_post_data:
            self.send_response(304)
            self.delete_cookie('messages')
            return
        self.send_response(200)

    def delete_cookie(self, key):
        self.send_header('Set-Cookie', f'{key}=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')

def main():
    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print('Serving HTTP on port 8000...')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print_stacktrace(KeyboardInterrupt)

if __name__ == '__main__':
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

if __name__ == '__main__':
    try:
        # Send a POST request to the server
        import requests
        response = requests.post('http://localhost:8000', data='messages=Hello')
        if response.status_code != 304:
            raise AssertionError("Expected status code 304, but got {}".format(response.status_code))
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue reproduced successfully")
        exit(0)

```

This script sets up a simple HTTP server that responds to GET and POST requests. When a POST request is received, it checks if the 'messages' parameter is present in the query string. If it is, it sends a 304 response and deletes the cookie using the `delete_cookie` method. The script then attempts to send a POST request to the server with the 'messages' parameter and checks that the status code of the response is 304. If the status code is not 304, an AssertionError is raised, which will print a stack trace and exit with a non-zero status code.