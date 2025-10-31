from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.views.static import serve
import os

def repro_asgi_app():
    return {
        "ASGI": {
            "http": {"class": "daphne.http.Server", "config": {}},
            "https": {"class": "daphne.http.Server", "config": {}}
        }
    }

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

if __name__ == '__main__':
    try:
        settings.configure()
        from django.urls import re_path
        from asgiref import ASGIApplication
        app = repro_asgi_app()
        ASGIApplication(app)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected warning"
