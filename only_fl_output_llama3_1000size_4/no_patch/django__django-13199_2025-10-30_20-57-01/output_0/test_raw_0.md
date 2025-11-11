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
        post_body = self.rfile.read(content_length).decode('utf-8')
        query_params = parse_qs(urlparse(post_body).query)
        if 'messages' in query_params:
            self.send_response(304)
            self.send_header('Set-Cookie', 'messages=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
            self.end_headers()
        else:
            self.send_response(200)

def main():
    with http.server.HTTPServer(('localhost', 8000), TestRequestHandler) as httpd:
        print('Serving at port 8000...')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```

This script creates a simple HTTP server that responds to GET and POST requests. When the POST request contains a 'messages' parameter, it sets a cookie with SameSite set to Lax. Then, when the same request is made again (which should delete the cookie), the HttpResponse.delete_cookie() method does not preserve the SameSite attribute, resulting in a warning message from Firefox.

To run this script, save it as `reproducer.py` and execute it using `python3 reproducer.py`.