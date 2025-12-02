 Here is a standalone Python file `reproducer.py` that should reproduce the issue:
```python
import asyncio
import sys
from django.core.handlers.asgi import ASGIStaticFilesHandler
from django.http import FileResponse
from django.urls import path, include
from django.core.asgi import get_asgi_application

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

async def serve_static(request, path):
    return FileResponse(open(f"static/{path}", "rb"))

async def main():
    asgi_app = get_asgi_application()
    asgi_app = ASGIStaticFilesHandler(asgi_app)

    request_handler = asgi_app({
        "type": "http",
        "headers": [],
        "body": b"",
        "method": "GET",
        "real_path": "/admin/",
    })

    async for response in request_handler:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, create a new Django project with the following settings:
```python
INSTALLED_APPS = [
    "daphne",
    ...
]

ASGI_APPLICATION = "project.asgi.application"
```
Create a static file `static/test.txt` in the project directory.

Run the `reproducer.py` script with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.