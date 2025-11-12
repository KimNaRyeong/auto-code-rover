import django
from django.conf import settings
from django.urls.base import get_resolver

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
    settings.configure()
    settings.STATIC_URL = "http://minio/static/"
    try:
        get_resolver().urlconf_module
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Django adds spurious '/' prefix to settings.STATIC_URL='http://server/'")

if __name__ == "__main__":
    main()
