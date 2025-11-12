Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.core.wsgi import get_wsgi_application
from daphne.cli import CommandLineInterface
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    from reproducer import settings

    application = get_wsgi_application()
    asgi_app = ASGIStaticFilesHandler(application)

    cli = CommandLineInterface(asgi_app, input_fd=None)
    try:
        cli.run(['runserver', '--bind', '0.0.0.0:8000'])
    except Warning as w:
        print_stacktrace(w)
        assert False, "ASGIStaticFilesHandler raises warning"
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
```
<|start_header_id|>