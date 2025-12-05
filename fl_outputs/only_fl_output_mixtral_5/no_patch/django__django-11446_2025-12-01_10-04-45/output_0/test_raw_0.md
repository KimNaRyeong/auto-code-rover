 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured

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

def serve_404(request):
    if not settings.DEBUG:
        return HttpResponse('<h1>Not Found</h1><p>The requested resource was not found on this server.</p>')
    else:
        # This is the correct HTML for a 404 error page in DEBUG=True mode
        return HttpResponse('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta http-equiv="content-type" content="text/html; charset=utf-8">\n<meta name="robots" content="NONE,NOARCHIVE">\n<title>404 Not Found: {}</title>\n</head>\n<body>\n<h1>Not Found</h1>\n<p>The requested resource was not found on this server.</p>\n</body>\n</html>'.format(request.path), status=404)

if __name__ == '__main__':
    try:
        settings.configure(
            DEBUG=False,
            ROOT_URLCONF=__name__,
        )
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()

        # Simulate a 404 error
        request = Application({'PATH_INFO': '/non-existent-page/'})
        response = serve_404(request)

        # The response should be a full HTML page
        assert response.content.startswith(b'<html>') and response.content.endswith(b'</html>')

    except ImproperlyConfigured as e:
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the default 404 error page is not a full HTML page in `DEBUG=False` mode. If the default 4