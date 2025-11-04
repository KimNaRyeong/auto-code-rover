Here is the reproducer script:

```python
import requests
import unittest
from OpenSSL import SSL
from urllib3.exceptions import HTTPError
from io import BytesIO
from http.client import HTTPResponse
from unittest.mock import patch, Mock

class TestRedirect(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_pyopenssl_redirect(self, urlopen):
        response = Mock(spec=HTTPResponse)
        response.getheader.return_value = '301 Moved Permanently'
        response.getcode.return_value = 301
        response.read.return_value = b''

        urlopen.return_value = response

        s = SSL.Connection()
        s.set_connect_state()
        s.set_accept_state()

        buf = BytesIO(b'GET /redirect/1 HTTP/1.1\r\nHost: httpbin.org\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nUser-Agent: python-requests/2.2.1 CPython/2.7.6 Windows/8\r\n\r\n')

        with self.assertRaises(TypeError):
            s.sendall(buf.getvalue(), 0)

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` module to create a test case that reproduces the issue. It mocks out the `urllib.request.urlopen` function and creates an `HTTPResponse` object with a status code of 301 and no body. The script then attempts to send the response using the `sendall` method, which should raise a `TypeError` because the buffer is not bytes.

To run this script, save it in a file named `reproducer.py`, navigate to that directory in your terminal or command prompt, and execute the script with the command `python3 reproducer.py`.