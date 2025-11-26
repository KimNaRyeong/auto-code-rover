import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

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

settings.configure(
    STATIC_URL="http://minio/static/",
    INSTALLED_APPS=['django.contrib.staticfiles'],
)

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from django.templatetags.static import static
    url = static('images/app-icons/favicon.ico')
    assert not url.startswith('/http:'), f"STATIC_URL has spurious '/' prefix: {url}"
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("Issue is fixed!")
raise SystemExit(0)
