Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import requests
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8000/')
        self.end_headers()
        self.wfile.write('')

def run_https_server():
    httpd = HTTPServer(('localhost', 4443), RedirectHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='yourpemfile.pem')
    httpd.serve_forever()

def run_http_server():
    def handler(*args):
        return "HTTP Server"
    httpd = HTTPServer(('localhost', 8000), handler)
    httpd.serve_forever()

def test_redirect():
    threading.Thread(target=run_https_server).start()
    threading.Thread(target=run_http_server).start()

    try:
        response = requests.get('https://localhost:4443', auth=('hello', 'world'), verify=False)
        assert 'Authorization' not in response.request.headers, "Authorization header was not stripped"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_redirect()
```
This script sets up an HTTPS server on `localhost:4443` that redirects to `http://localhost:8000`, and a plain HTTP server on `localhost:8000`. It then makes a request to the HTTPS server with basic auth credentials, and checks if the `Authorization` header is present in the redirected request. If it is, an `AssertionError` is raised, printing a stack trace of the issue.

Note that you'll need to replace `'yourpemfile.pem'` with the path to your SSL certificate file.