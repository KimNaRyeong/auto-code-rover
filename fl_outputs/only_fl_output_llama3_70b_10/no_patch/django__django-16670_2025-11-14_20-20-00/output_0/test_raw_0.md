Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application
from daphne.cli import Command as DaphneCommand

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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])

    from project.asgi import application
    from django.core.handlers.asgi import ASGIStaticFilesHandler

    app = ASGIStaticFilesHandler(application)

    try:
        async def call_app():
            await app({'type': 'http'}, {'method': 'GET', 'path': '/admin/'})
        import asyncio
        loop = asyncio.get_event_loop()
        task = loop.create_task(call_app())
        loop.run_until_complete(task)
    except Warning as e:
        print_stacktrace(e)
        assert False, "ASGIStaticFilesHandler raises warning"

if __name__ == "__main__":
    main()
```
<|start_header_id|>