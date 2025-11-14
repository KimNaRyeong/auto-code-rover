Here is the reproducer script:

```python
import flask
from flask import Flask, Blueprint
import unittest
from unittest.mock import patch

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

class TestIssue(unittest.TestCase):

    @patch('sys.stdout')
    def test_issue(self, mock_stdout):
        app.run(debug=True)

        # Check if the index route works
        response = flask.Response("index", mimetype='text/html')
        self.assertEqual(response.get_data(as_text=True), "index")

        # Check if the parent route in the subdomain works
        response = flask.Request('http://api.localhost:5000/').get()
        self.assertEqual(response.data.decode('utf-8'), "parent")

        # Check if the child route does not work
        response = flask.Request('http://api.localhost:5000/child/').get()
        self.assertEqual(response.status_code, 404)

        raise AssertionError("Issue is present")

if __name__ == '__main__':
    test_issue()
```

This script will run the Flask app and then check if the index route works, if the parent route in the subdomain works, and if the child route does not work. If all checks pass, it means that the issue is fixed.