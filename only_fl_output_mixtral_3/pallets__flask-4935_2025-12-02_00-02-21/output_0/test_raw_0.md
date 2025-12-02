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
        exit(1)
```
When you run this script with `python3 reproducer.py` and access `http://api.localhost:5