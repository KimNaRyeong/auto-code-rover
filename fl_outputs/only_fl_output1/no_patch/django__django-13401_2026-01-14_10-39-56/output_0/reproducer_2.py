# reproducer.py
import sys

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

def setup_django_environment():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=['__main__'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
    )

    import django
    django.setup()

def define_models():
    from django.db import models

    class A(models.Model):
        myfield = models.IntegerField()

        class Meta:
            abstract = True

    class B(A):
        pass

    class C(A):
        pass

    return B, C

def main():
    setup_django_environment()
    B, C = define_models()

    try:
        # Check if the fields myfield from both B and C compare equal.
        field_b = B._meta.get_field('myfield')
        field_c = C._meta.get_field('myfield')
        fields_set = {field_b, field_c}
        assert len(fields_set) == 2, "Abstract model fields 'myfield' from B and C are considered equal."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code when the issue is present

    print("Issue fixed.")
    sys.exit(0)  # Exit with success code when the issue is fixed.

if __name__ == "__main__":
    main()
