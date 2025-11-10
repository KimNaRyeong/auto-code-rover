Here is the reproducer script:

```python
import requests
import unittest
from io import BytesIO
from unittest.mock import patch, Mock

class TestReproducer(unittest.TestCase):
    def test_reproducer(self):
        with patch('requests.post') as mock_post:
            response = Mock()
            response.content = b'content'
            response.status_code = 200
            response.reason = 'OK'
            response.encoding = None
            response._content_consumed = True

            mock_post.return_value = response

            try:
                response.content
            except Exception as e:
                print_stacktrace(e)
                self.fail('Expected exception')

            with self.assertRaises(Exception):
                response.content

    def print_stacktrace(self, e: Exception):
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

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` module to create a test case. It mocks the `requests.post` function using the `patch` decorator from the `unittest.mock` module, and sets up a mock response object with some expected attributes.

The test case then attempts to access the `response.content` attribute twice, expecting an exception on the first attempt and another exception on the second attempt. If the issue is present, it prints the stack trace using the `print_stacktrace` function and fails the test.