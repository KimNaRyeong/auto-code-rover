```python
import os
import sys
import django
from django.conf import settings
from django.core.management import call_command
from django.db import models, OperationalError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dynamically configure the Django settings
def setup_django():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=('__main__',),
        ROOT_URLCONF='__main__',
        MIDDLEWARE=(),
    )
    django.setup()


def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


# Define initial models
class Bar(models.Model):
    pass


class Foo(models.Model):
    bar = models.ManyToManyField('Bar', blank=True)


def perform_initial_migration():
    call_command('makemigrations', '__main__', verbosity=0)
    call_command('migrate', verbosity=0)


# Modify Foo to reference itself
def modify_models():
    global Foo
    Foo = type('Foo', (models.Model,), {'bar': models.ManyToManyField('self', blank=True)})


def perform_secondary_migration():
    call_command('makemigrations', '__main__', verbosity=0)
    call_command('migrate', verbosity=0)


def test_issue_present():
    try:
        foo_instance = Foo.objects.create()
        foo_instance.bar.add(foo_instance)
        foo_instance.save()
    except OperationalError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present") from e


if __name__ == "__main__":
    setup_django()
    perform_initial_migration()

    # Clear models cache to prevent schema generation issues
    apps = django.apps.apps
    apps.all_models['__main__'].clear()
    apps.clear_cache()

    modify_models()
    perform_secondary_migration()

    # Test for issue
    try:
        test_issue_present()
    except AssertionError as e:
        sys.exit(1)  # Issue is present
    else:
        print("Issue is fixed.")
        sys.exit(0)
```