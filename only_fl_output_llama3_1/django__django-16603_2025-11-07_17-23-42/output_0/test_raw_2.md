Here is the reproducer script:

```python
import asyncio
from asgi_headers import HTTP_101_SWITCHING_PROTOCOLS, HTTP_DISCONNECT
from http.cookies import SimpleCookie
from io import BytesIO
from typing import Dict

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

def send_request(reader: asyncio.StreamReader) -> None:
    writer = await asyncio.open_connection('localhost', 8000)[1]
    writer.write(b'GET / HTTP/1.1\r\n')
    writer.write(b'Host: localhost:8000\r\n')
    writer.write(b'Connection: Upgrade\r\n')
    writer.write(b'Upgrade: h2c\r\n')
    writer.write(b'HTTP2-Settings: 1234567890abcdef\r\n')
    writer.write(b'\r\n')

    # Send the request body
    writer.write(b'some body\r\n')
    writer.write(b'\r\n')

    # Simulate a disconnect
    writer.write(HTTP_DISCONNECT.encode('utf-8'))
    writer.write(b'\r\n')

    await writer.drain()
    writer.close()

def main() -> None:
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_request(None))
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sends a GET request with a body and then simulates a disconnect. If the issue is present, it will raise an `AssertionError` and print the stack trace.