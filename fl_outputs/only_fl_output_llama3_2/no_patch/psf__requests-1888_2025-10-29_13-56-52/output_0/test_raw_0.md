Here is the reproducer script:

```python
import requests
import unittest
from OpenSSL import SSL
from urllib3.exceptions import HTTPError
from io import BytesIO
from contextlib import redirect_stdout, redirect_stderr

class TestRedirect(unittest.TestCase):

    def test_pyopenssl_redirect(self):
        with self.assertRaises(HTTPError) as e:
            response = requests.get('https://httpbin.org/status/301', stream=True)
            f = BytesIO()
            with redirect_stdout(f), redirect_stderr(f):
                response.raise_for_status()

        print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.