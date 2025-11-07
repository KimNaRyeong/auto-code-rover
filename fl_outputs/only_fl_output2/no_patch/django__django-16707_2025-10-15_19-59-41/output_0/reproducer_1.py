# reproducer.py
import os
import django
from django.conf import settings

def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        USE_I18N=True,
    )
    django.setup()

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

def test_datefield_input_formats_str():
    from django.forms.fields import DateField
    try:
        input_formats_str = str(DateField().input_formats)
        print(input_formats_str)  # Attempt to use __str__ method, which should fail if the issue is present.
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("DateField input_formats cannot be printed using __str__") from e

if __name__ == '__main__':
    setup_django_environment()
    test_datefield_input_formats_str()
