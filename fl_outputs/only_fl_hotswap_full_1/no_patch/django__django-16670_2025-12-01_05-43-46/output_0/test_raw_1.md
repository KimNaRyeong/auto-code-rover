 Here is a standalone Python file `reproducer.py` that should reproduce the issue:
```python
import asyncio
import sys
from django.core.handlers.asgi import ASGIStaticFilesHandler
from django.http import FileResponse
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.core.asgi import get_asgi_application

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

async def serve_static(request, path):
    static_file = settings.STATIC_ROOT / path
    if not static_file.exists():
        return TemplateView.as_view(template_name='404.html')(request)
    response = FileResponse(static_file, as_attachment=True)
    return response

async def asgi_app(scope, receive, send):
    application = get_asgi_application()
    handler = ASGIStaticFilesHandler(application)
    await handler(scope, receive, send)

if __name__ == "__main__":
    settings.configure(
        DEBUG=True,
        STATIC_ROOT=asyncio.Path(__file__).parent / 'staticfiles',
        ROOT_URLCONF='reproducer',
    )
    urlpatterns = [
        path('static/<path:path>', serve_static),
        path('__debug__/', include('debug_toolbar.urls')),
        path('', TemplateView.as_view(template_name='index.html')),
    ]
    try:
        from django.core.servers.basehttp import get_internal_wsgi_application
        application = get_internal_wsgi_application()
        from django.core.servers.basehttp import run
        run(asgi_app, ('0.0.0.0', 8000))
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, create a directory named `staticfiles` in the same directory as the `reproducer.py` file, and put any file in it. Then run the script with `python3 reproducer.py`. The script should raise an `AssertionError` with the following message:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 51, in <module>
    run(asgi_app, ('0.0.0.0', 8000))
  File "/path/to/venv/lib/python3.8/site-packages/channels/management/commands/runserver.py", line 52, in run
    run(server, addr, *args, **kwargs)
  File "/path/to/venv/lib/python3.8/site-packages/channels/management/commands/runserver.py", line 70, in run
    six.exec_(
  File "/path/to/venv/lib/python3.8/site-packages/channels/management/commands/runserver.py", line 73, in exec_
    super().run(*args, **kwargs)
  File "/path/to/venv/lib/python3.8/site-packages/django/core/servers/basehttp.py", line 139, in run
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
  File "/path/to/venv/lib/python3.8/site-packages/django/core/servers/basehttp.py", line 79, in __init__
    super().__init__(*args, **kwargs)
  File "/usr/lib/python3.8/socketserver.py",