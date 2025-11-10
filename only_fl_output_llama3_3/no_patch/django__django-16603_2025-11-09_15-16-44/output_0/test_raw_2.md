Here is the reproducer script:

```python
import asyncio
import tempfile
from django.core.handlers.asgi import ASGIServer

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
    body_file = tempfile.SpooledTemporaryFile(max_size=1024*1024, mode="w+b")
    while True:
        message = await receive()
        if message["type"] == "http.disconnect":
            body_file.close()
            raise AssertionError("http.disconnect not handled on requests with body")
        if "body" in message:
            body_file.write(message["body"])
        if not message.get("more_body", False):
            break
    body_file.seek(0)
    return body_file

async def main():
    server = ASGIServer(read_body, host="localhost", port=8000)

try:
    asyncio.run(main())
except Exception as e:
    print_stacktrace(e)
else:
    print("Issue not present")
```

This script creates an ASGI server that handles requests with bodies and sends http.disconnect messages. If the issue is present, it will raise an AssertionError, which will be caught and printed using the provided function.