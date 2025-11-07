```python
# reproducer.py

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

def setup_django_environment():
    import os
    import django
    from django.conf import settings
    from django.db import models
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'db.sqlite3')

    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': db_path,
            }
        },
        INSTALLED_APPS=[
            __name__,  # Allow Django to find and create the test model tables
        ],
        USE_TZ=True,
    )

    django.setup()

    class Foo(models.Model):
        a = models.CharField(max_length=100)
        d = models.IntegerField()

    class Bar(models.Model):
        a = models.ForeignKey(Foo, on_delete=models.CASCADE)
        b = models.CharField(max_length=100)
    
    return Foo, Bar

def reproduce_issue():
    Foo, Bar = setup_django_environment()

    from django.core.management import call_command
    call_command('migrate', interactive=False, verbosity=0)

    try:
        foo1 = Foo.objects.create(a='foo1', d=1)
        foo2 = Foo.objects.create(a='foo2', d=2)
        bar1 = Bar.objects.create(a=foo1, b='bar1')

        import copy
        bar2 = copy.copy(bar1)
        bar2.pk = None
        bar2.a = foo2

        # Assertions that fail on Django >= 2.0
        assert bar2.a == foo2, "bar2 does not point to foo2"
        assert bar2.a_id == foo2.id, "bar2.a_id does not match foo2.id"
        
        # These fail due to the reported issue
        assert bar1.a == foo1, "bar1 does not point to foo1 after copying"
        assert bar1.a_id == foo1.id, "bar1.a_id does not match foo1.id"
        
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Ensure non-zero exit code for failure

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a minimal Django environment within the script, defines two simple model classes, `Foo` and `Bar`, where `Bar` has a ForeignKey reference to `Foo`. It then attempts to reproduce the issue described by copying an instance of a model using `copy.copy()` and manipulating the foreign key fields. Assertion errors are used to validate the expectations for both the original and copied instances, and if an assertion fails, it prints a detailed stack trace to help diagnose the issue more clearly and exits with a non-zero status code to indicate an error state. This script is intended to be a self-contained way to replicate the ForeignKey caching behavior change issue observed when upgrading from Django 1.11.x to Django 2.x.