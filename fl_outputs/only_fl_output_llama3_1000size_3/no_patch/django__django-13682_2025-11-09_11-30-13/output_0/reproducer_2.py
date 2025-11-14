from django.urls import path
from django.views.generic.base import View

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

class EmptyCBView(View):
    pass

def main():
    urlpatterns = [path('home', EmptyCBView)]
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        resolver.url_patterns  # This should raise an error
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue should be present"

if __name__ == "__main__":
    main()
