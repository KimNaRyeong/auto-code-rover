Here is the reproducer script:

```python
import requests
import unittest
from OpenSSL import SSL
from urllib3.exceptions import HTTPError
from io import BytesIO
from contextlib import redirect_stdout, redirect_stderr
import sys
import traceback
import os

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestRedirect(unittest.TestCase):

    def test_pyopenssl_redirect(self):
        try:
            response = requests.get('https://httpbin.org/status/301', stream=True)
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            with BytesIO() as f, redirect_stdout(f), redirect_stderr(f):
                print_stacktrace(e)
            raise

if __name__ == '__main__':
    unittest.main()
```

To run the script, save it to a file named `reproducer.py` and execute it using Python: `python3 reproducer.py`.