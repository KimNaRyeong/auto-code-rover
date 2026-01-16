import django
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Setup Django environment
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # Register this module as an app
    ),
    USE_I18N=False,
    USE_L10N=False,
    USE_TZ=False,
)

django.setup()

class Test(models.Model):
    char_field = models.CharField(max_length=None)

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
        # Attempt to create the Test model, which is expected to fail validation
        test = Test()
        test.full_clean()  # This should trigger validation
    except ValidationError as e:
        print_stacktrace(e)
        raise AssertionError("An error occurred, CharField with max_length=None should not raise ValidationError") from e

    print("No ValidationError raised for CharField with max_length=None, issue seems to be fixed.")

if __name__ == '__main__':
    main()
