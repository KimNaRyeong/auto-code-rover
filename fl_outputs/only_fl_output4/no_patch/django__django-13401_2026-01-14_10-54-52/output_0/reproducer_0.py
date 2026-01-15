# reproducer.py

from django.db import models
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        '__main__',  # Adding our temporary module to Django's INSTALLED_APPS
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

import django
django.setup()

class A(models.Model):
    class Meta:
        abstract = True
    myfield = models.IntegerField()

class B(A):
    pass

class C(A):
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
        assert len({B._meta.get_field('myfield'), C._meta.get_field('myfield')}) == 2, "Fields should not compare equal"
        print("Issue seems to be fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate an issue

if __name__ == '__main__':
    main()
