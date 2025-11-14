import django
from django.urls import path, re_path
from django.urls.resolvers import get_resolver
from django.urls.base import resolve

def MyView():
    pass

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
    try:
        urlpatterns = [
            path("path/to/thing", MyView.as_view(), "my_view"),
        ]
        resolve("/path/to/thing")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected ValueError or TypeError")

if __name__ == "__main__":
    main()
