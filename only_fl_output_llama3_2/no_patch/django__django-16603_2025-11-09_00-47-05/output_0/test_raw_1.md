Here is the reproducer script:

```python
import asyncio
import tempfile
import settings  # Assuming this module has FILE_UPLOAD_MAX_MEMORY_SIZE setting
from django.core.handlers.asgi import ASGIHandler

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

async def read_body(receive):
    body_file = tempfile.SpooledTemporaryFile(max_size=settings.FILE_UPLOAD_MAX_MEMORY_SIZE, mode="w+b")
    while True:
        message = await receive()
        if message["type"] == "http.disconnect":
            body_file.close()
            raise AssertionError("Expected http.disconnect to be handled")
        if "body" in message:
            body_file.write(message["body"])
        if not message.get("more_body", False):
            break
    body_file.seek(0)
    return body_file

async def main():
    handler = ASGIHandler()
    await read_body(handler.asgi_receive)

try:
    asyncio.run(main())
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will run an ASGI application that handles HTTP requests with bodies and disconnects. If the `http.disconnect` message is not handled correctly, it should raise an `AssertionError`, which will be caught by the script and printed to the console along with a stack trace.