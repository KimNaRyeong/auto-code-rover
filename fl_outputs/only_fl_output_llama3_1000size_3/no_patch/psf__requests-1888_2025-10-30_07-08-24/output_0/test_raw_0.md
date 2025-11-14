Here is the reproducer script:

```python
import requests
import unittest
from OpenSSL import SSL
from urllib3.exceptions import HTTPError
from unittest.mock import patch, Mock

class TestRedirect(unittest.TestCase):
    @patch('urllib3.connectionpool.PoolManager')
    def test_pyopenssl_redirect(self, pool_manager_mock):
        # Create a mock connection to simulate the redirect
        connection = Mock()
        connection.get_response.return_value.status_code = 301
        connection.get_response.return_value.headers['Location'] = 'https://example.com/new-location'
        
        # Set up the requests adapter to use our mock connection
        adapter = requests.adapters.HTTPAdapter()
        adapter.pool_manager = pool_manager_mock
        requests.session().mount('https://', adapter)
        
        try:
            response = requests.get('https://httpbin.org/status/301')
            self.fail("Expected an exception")
        except HTTPError as e:
            print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

This script creates a mock connection that simulates the redirect and sets up the requests adapter to use this mock connection. It then attempts to make a GET request to 'https://httpbin.org/status/301' and expects an exception to be raised, which it prints using the provided `print_stacktrace` function.

To run the script, save it in a file named `reproducer.py` and execute it with Python: `python3 reproducer.py`.