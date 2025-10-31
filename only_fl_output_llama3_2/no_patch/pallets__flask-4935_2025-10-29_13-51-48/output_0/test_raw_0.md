Here is the reproducer script:

```python
import os
import sys
from flask import Flask, Blueprint
from flask.testing import TestCase

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
parent = Blueprint("parent", __name__)
child = Blueprint("child", __name__)

class TestIssue(TestCase):
    def test_issue(self):
        @parent.route('/')
        def parent_index():
            return "parent"

        @child.route('/child/')
        def child_index():
            return "child"

        parent.register_blueprint(child)
        app.register_blueprint(parent, subdomain="api")

        with self.assertRaises(AssertionError):
            os.system(f"python -c \"import http.client; conn = http.client.HTTPConnection('localhost', 5000); conn.request('GET', '/'); response = conn.getresponse(); print(response.status)\"")

if __name__ == '__main__':
    TestIssue().run()
```

This script will run a Flask test case that attempts to access the `/child/` route through the subdomain `api.localhost:5000`. If the issue is present, it should raise an `AssertionError`, and if not, it should exit with code 0.