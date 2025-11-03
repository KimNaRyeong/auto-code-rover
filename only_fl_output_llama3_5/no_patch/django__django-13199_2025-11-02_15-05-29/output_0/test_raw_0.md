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
            self.delete_cookie('messages')

    def delete_cookie(self, key):
        self.send_header('Set-Cookie', f'{key}=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/')
        self.end_headers()

def main():
    with http.server.HTTPServer(('', 8000), TestRequestHandler) as httpd:
        print('Serving HTTP on port 8000...')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
```

You can run this script by executing `python3 reproducer.py`. This will start a simple HTTP server that listens on port 8000. You can test the issue by sending a POST request to `http://localhost:8000/` with a query parameter `messages`. The server should respond with a 304 status code and delete the cookie using the `delete_cookie` method, which does not preserve the `SameSite` attribute.

To reproduce the issue, you can use a tool like `curl` or a web browser to send the POST request. For example:

```
curl -X POST 'http://localhost:8000/' -d "messages=Hello&foo=bar"
```

This should trigger the warning message in Firefox about the cookie being soon rejected because it has the `SameSite` attribute set to `None`.