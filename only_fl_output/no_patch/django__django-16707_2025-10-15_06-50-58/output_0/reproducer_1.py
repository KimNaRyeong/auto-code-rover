# reproducer.py
import os
import sys
import django
from django.conf import settings

# Minimal required Django settings
MINIMAL_SETTINGS = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'DEBUG': True,
    'ROOT_URLCONF': __name__,  # We don't use urls but this is a required setting
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
        }
    },
    'SITE_ID': 1,
}

# Apply minimal Django settings if not already configured
if not settings.configured:
    settings.configure(**MINIMAL_SETTINGS)
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

def test_input_format_str_representation():
    from django.forms.fields import DateField
    
    try:
        # Attempt to print the string representation of DateField.input_formats
        str_representation = str(DateField().input_formats)
        print("Successfully obtained string representation:", str_representation)
        
        # No exception means issue is presumably fixed. Exit with code 0.
        exit(0)
        
    except Exception as e:
        # If any exception occurred, print stacktrace and raise AssertionError.
        print_stacktrace(e)
        raise AssertionError("Failed to convert DateField.input_formats to string") from e
        
if __name__ == "__main__":
    test_input_format_str_representation()
