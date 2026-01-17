# reproducer.py
import os
import sys
import django
from django.conf import settings

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

def setup_django_settings():
    settings.configure(
        DEBUG=True,
        LANGUAGE_CODE='en',
        LANGUAGES=[('en', 'English')],
        LANGUAGES_BIDI=['he', 'ar', 'fa', 'ur'],
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
        ],
        # Include additional necessary settings
    )

def run_test():
    from django.core.checks.translation import check_language_settings_consistent
    
    try:
        # Setup Django settings
        setup_django_settings()
        django.setup()
        
        errors = check_language_settings_consistent(None)
        
        # Assuming the desired state is no errors returned
        assert not errors, "Errors found in language settings consistency check"
        
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
    print("No issues found - the check passed successfully.")
    sys.exit(0)
