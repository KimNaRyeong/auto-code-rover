import os
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from unittest.mock import patch, Mock
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
        max_post_process_passes = 0

    settings_configured = False
    try:
        if not settings.configured:
            settings.configure()
            settings_configured = True
        
        settings.STATICFILES_STORAGE = "MyManifestStaticFilesStorage"
        
        call_command('collectstatic', verbosity=0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

    if not settings_configured:
        print("Settings were not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.")
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not reproduced. Exiting with code 0.")
        sys.exit(0)
