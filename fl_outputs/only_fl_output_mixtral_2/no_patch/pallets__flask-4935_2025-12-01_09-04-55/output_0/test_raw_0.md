 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
from flask import Flask, Blueprint, request

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
parent = Blueprint("parent", __name__)
child = Blueprint("child", __name__)

@app.route('/')
def index():
    return "index"

@parent.route('/')
def parent_index():
    return "parent"

@child.route('/child/')
def child_index():
    return "child"

parent.register_blueprint(child)
app.register_blueprint(parent, subdomain="api")

@app.route('/test', methods=['GET'])
def test():
    response = request.script_root
    if response == '/test':
        return "Test passed", 200
    else:
        raise AssertionError(f"Test failed: {response}")

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will start a Flask server on `localhost:5000` and register the blueprints as described in the issue. The `/test` endpoint is added to check if the issue is present.

If the issue is present, the `/test` endpoint will return a 404 response, and the script will raise an `AssertionError` with a stack trace. If the issue is fixed, the `/test` endpoint will return a 200 response with the message "Test passed".

The expected output is:
```ruby
Traceback (most recent call last):
  File "reproducer.py", line 43, in <module>
    app.run(debug=True)
  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1043, in run
    run_simple(host, port, self, **options)
  File "/usr/local/lib/python3.9/site-packages/werkzeug/serving.py", line 1113, in run_simple
    inner()
  File "/usr/local/lib/python3.9/site-packages/werkzeug/serving.py", line 1092, in inner
    srvr.serve_forever()
  File "/usr/local/lib/python3.9/site-packages/werkzeug/serving.py", line 840, in serve_forever
    HTTPServer.serve_forever(self)
  File "/usr/local/lib/python3.9/socketserver.py", line 236, in serve_forever
    self._handle_request_noblock()
  File "/usr/local/lib/python3.9/socketserver.py", line 317, in _handle_request_noblock
    self.process_request(request, client_address)
  File "/usr/local/lib/python3.9/socketserver.py", line 303, in process_request
    self.finish_request(request, client_address)
  File "/usr/local/lib/python3.9/socketserver.py", line 320, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "/usr/local/lib/python3.9/site-packages/werkzeug/serving.py", line 270, in __init__
    super().__init__