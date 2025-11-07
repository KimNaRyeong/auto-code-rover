Here is the reproducer script:

```python
import requests
import unittest
from OpenSSL import SSL

class TestIssue(unittest.TestCase):

    def test_issue(self):
        try:
            response = requests.get('https://httpbin.org/status/301', verify=False)
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")

if __name__ == '__main__':
    unittest.main()
```

You can run this script using `python3 reproducer.py`. If the issue is present, it will print a stack trace and exit with code 1. If the issue is fixed, it will exit with code 0.