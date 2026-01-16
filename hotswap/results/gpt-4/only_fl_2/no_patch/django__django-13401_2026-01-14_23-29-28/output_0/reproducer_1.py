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

def setup_django():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            '__main__',  # Required for Django to recognize models defined here
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        USE_I18N=True,
        USE_L10N=True,
    )

    import django
    django.setup()

    from django.db import models

    class A(models.Model):
        class Meta:
            abstract = True
        myfield = models.IntegerField()

    class B(A):
        pass

    class C(A):
        pass

    return B, C

def main():
    B, C = setup_django()

    try:
        # Accessing fields after setup to avoid any setup-related issues
        field_b = B._meta.get_field('myfield')
        field_c = C._meta.get_field('myfield')

        assert field_b != field_c, "Fields from B and C should not compare as equal."

        assert len({field_b, field_c}) == 2, "Fields from B and C are wrongly deduplicated in a set."

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code if issue is present

if __name__ == "__main__":
    main()
    print("Issue not present, exited with code 0.")
