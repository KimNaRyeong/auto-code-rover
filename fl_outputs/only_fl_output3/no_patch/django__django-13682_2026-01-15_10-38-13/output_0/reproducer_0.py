# reproducer.py
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import execute_from_command_line

# Minimal Django setup for demonstration
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='foobar',
    ALLOWED_HOSTS=['*'],
)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


# Attempt to add a class-based view without calling .as_view()
urlpatterns = [
    path('home', HomeView),
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


def main():
    try:
        execute_from_command_line(['', 'check'])
    except ImproperlyConfigured as e:
        if 'as_view()' in str(e):
            # Issue fixed, this is the expected message
            print("Issue fixed.")
            exit(0)
        else:
            # Print stack trace if any other ImproperlyConfigured exceptions occurred
            print_stacktrace(e)
            exit(1)
    except Exception as e:
        # Print stack trace for any other exceptions
        print_stacktrace(e)
        exit(1)

    # If the exception related to .as_view() missing is not caught, it means the issue persists
    assert False, "Issue is present"


if __name__ == '__main__':
    main()
