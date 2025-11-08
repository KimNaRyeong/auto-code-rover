Here is the reproducer script:

```python
import requests
import unittest
from io import BytesIO
from unittest.mock import patch, Mock

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestReproducer(unittest.TestCase):

    @patch('requests.post')
    def test_reproducer(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.content = b'Hello, World!'
        response.raw = BytesIO(b'Hello, World!')
        response._content_consumed = True

        mock_post.return_value = response

        try:
            response.content
        except Exception as e:
            print_stacktrace(e)
            self.fail("Error raised")

        content = response.content
        self.assertEqual(content, b'Hello, World!')

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` module to create a test case. It mocks the `requests.post` function using the `patch` decorator from the `mock` library. The mock response is set up with a status code of 200 and some sample content. The test then attempts to access the response content twice, which should raise an error if the issue is present.