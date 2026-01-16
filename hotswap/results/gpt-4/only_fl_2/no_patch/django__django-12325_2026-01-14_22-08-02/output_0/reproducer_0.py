# reproducer.py

def main():
    import django
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    from django.db import models

    # Minimal Django setup
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=('__main__',),
        USE_I18N=False,
        USE_L10N=False,
        USE_TZ=False,
    )
    django.setup()

    # Define models to reproduce the issue
    class Document(models.Model):
        pass

    try:
        class Picking(Document):
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

        # If the code reaches this point without raising an Exception, the issue is considered fixed.
        print("Issue seems to be fixed.")
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e


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


if __name__ == "__main__":
    main()
