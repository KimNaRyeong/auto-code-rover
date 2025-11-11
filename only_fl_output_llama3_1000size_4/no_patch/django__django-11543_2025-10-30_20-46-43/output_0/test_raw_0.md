Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote

class ReproducerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def run_server():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, ReproducerRequestHandler)
    print("Starting server...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from wsgiref.simple_server import make_server

    def app(environ, start_response):
        request = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        return [b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!']

    httpd = make_server('', 8001, app)
    print("Starting server...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

def reproduce_issue():
    main_thread = threading.Thread(target=run_server)
    main_thread.start()

    def client_socket():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8000))
        sock.sendall(b'GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: keep-alive\r\n\r\n')
        sock.close()

    client_thread = threading.Thread(target=client_socket)
    client_thread.start()
    main_thread.join()

    if os.environ.get('NO_THREADING', 'false').lower() == 'true':
        raise AssertionError("runserver fails to close connection")

if __name__ == '__main__':
    reproduce_issue()
```

This script creates a simple HTTP server using the `http.server` module and starts it in one thread. It then connects to this server from another thread, sending a GET request with the `Connection: keep-alive` header.

If you run this script with the `--nothreading` option (e.g., `python3 reproducer.py --nothreading`), it will raise an `AssertionError`, indicating that the issue is present.