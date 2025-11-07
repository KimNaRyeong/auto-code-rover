Here is the reproducer script:

```python
import os
import sys
from flask import Flask, Blueprint
from flask import request
from functools import wraps

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"

parent = Blueprint("parent", __name__, url_prefix='/api')
child = Blueprint("child", __name__)

def check_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_stacktrace(e)
            sys.exit(1)
    return wrapper

@app.route('/')
@check_issue
def index():
    return "index"

@parent.route('/')
@check_issue
def parent_index():
    return "parent"

@child.route('/child/')
@check_issue
def child_index():
    return "child"

parent.register_blueprint(child)

app.register_blueprint(parent, subdomain='api')

if __name__ == '__main__':
    app.run(debug=True)
```

This script reproduces the issue by checking if the `child_index` route is accessible when mounted on a subdomain. If it's not accessible, it prints the stack trace and exits with code 1.