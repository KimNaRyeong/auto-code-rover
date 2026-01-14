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
    from django.conf import settings
    from django.core.management import execute_from_command_line
    from django.urls import path
    from django.http import HttpResponse
    from django.views import View

    # Define a simple Class-Based View without calling .as_view()
    class HomeView(View):
        def get(self, request):
            return HttpResponse("Hello, World")

    # Setup minimal Django settings
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        SECRET_KEY='foobar',
    )

    # Define URL pattern without calling .as_view() on CBV
    urlpatterns = [
        path('home', HomeView),  # This will cause the issue
    ]

    try:
        # Trying to simulate Django's URL check might trigger the error
        execute_from_command_line(['django-admin', 'check'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from None

if __name__ == "__main__":
    main()
