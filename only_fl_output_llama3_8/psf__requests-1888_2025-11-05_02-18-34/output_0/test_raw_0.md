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
        with redirect_stdout(BytesIO()) as stdout, redirect_stderr(BytesIO()) as stderr:
            try:
                response = requests.get('https://httpbin.org/status/301', stream=True)
                self.assertEqual(response.status_code, 200)
            except HTTPError as e:
                print_stacktrace(e)
                raise AssertionError("Issue present")

if __name__ == '__main__':
    unittest.main()
```

This script uses the `requests` library to send a GET request to `https://httpbin.org/status/301`. It then checks if the response status code is 200. If an HTTPError occurs during this process, it prints the stack trace and raises an AssertionError with the message "Issue present".