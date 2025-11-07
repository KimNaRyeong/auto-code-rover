import django
from django.conf import settings
from django.db import models
from django.db.models import Exists, Q
from django.core.exceptions import AppRegistryNotReady

# Configure Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

django.setup()

# Define a model
class Book(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'


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


def run_reproducer():
    # Attempt to reproduce the issue
    try:
        q = Q() & Exists(Book.objects.all())
        assert not q.negated  # passes

        q = Q() & ~Exists(Book.objects.all())
        assert q.negated  # supposed to fail here according to the issue description
        print("Issue not found.")
    except AssertionError as e:
        print_stacktrace(e)
        print("Issue reproduced.")
        exit(1)
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    run_reproducer()
