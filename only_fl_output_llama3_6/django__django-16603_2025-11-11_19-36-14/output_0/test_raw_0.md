Here is the reproducer script:

```python
import asyncio
import uvicorn
from uvicorn.main import run
from asgi_headers import HTTP_101_SWITCHING_PROTOCOLS, HTTP_200_OK
from http.cookies import SimpleCookie
from http.client import HTTPConnection
from unittest.mock import patch

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

@patch('uvicorn.main.run')
async def reproduce_issue(mock_run):
    app = uvicorn.load(u'example:app', config=uvicorn.Config(example.App, host='127.0.0.1', port=8000))
    connection = HTTPConnection('localhost', 8000)
    connection.request('POST', '/', body=b'some body')
    response = connection.getresponse()
    assert response.status == HTTP_200_OK
    connection.request('POST', '/', body=b'', headers={'Content-Length': '0'})
    response = connection.getresponse()
    assert response.status == HTTP_101_SWITCHING_PROTOCOLS
    connection.request('POST', '/', body=b'', headers={'Content-Length': '0'}, expect=100)
    response = connection.getresponse()
    print_stacktrace(response)

if __name__ == '__main__':
    reproduce_issue()
```

This script uses the `uvicorn` library to start an ASGI application, and then simulates a series of HTTP requests to test the issue. The `reproduce_issue` function is marked as async because it contains await expressions.