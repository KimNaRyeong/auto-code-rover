# reproducer.py
from django.urls import path, resolve
from django.http import HttpResponse
from django.views import View
from django.conf import settings

# Minimal setup for Django to work
settings.configure(
    ROOT_URLCONF=__name__,
    SECRET_KEY='foobar',
    DEBUG=True,
)

# A simple view to use with the path
class MyView(View):
    def get(self, request):
        return HttpResponse("Hello, World!")

# Create a URL pattern with the issue
urlpatterns = [
    path("path/to/thing", MyView.as_view(), "my_view"),
]


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


if __name__ == "__main__":
    try:
        resolve("/path/to/thing")
        print("Issue not present. Exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, TypeError), "Expected a TypeError due to incorrect kwargs."
