```python
# reproducer.py

import os
import sys
from django.conf import settings
from django.core.management import call_command

# Configure settings for Django project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
    ],
    STATIC_URL='/static/',
    STATIC_ROOT=os.path.join(BASE_DIR, 'static'),
    STATICFILES_STORAGE='__main__.MyManifestStaticFilesStorage',
    SECRET_KEY='very-secret-key',
)

# Import after configuring settings to avoid AppRegistryNotReady exception
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

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

def main():
    try:
        # Calling Django's collectstatic command programmatically
        call_command('collectstatic', interactive=False, verbosity=0)
        # If the command completes without errors, assertion will fail, indicating issue is fixed
        raise AssertionError("The issue does not manifest; `collectstatic` command succeeded.")
    except Exception as e:
        print_stacktrace(e)
        # Check for the specific UnboundLocalError we expect
        if 'local variable \'substitutions\' referenced before assignment' in str(e):
            sys.exit(0)  # Exit code 0 when issue is as expected
        else:
            raise  # Reraise exception if it's not the one we're looking for

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    # Mimic calling manage.py collectstatic for minimal setup
    execute_from_command_line([__file__, 'migrate'])  # Ensure db is ready even if not used
    main()
```

This script sets up a minimal Django environment programmatically, overrides the `STATICFILES_STORAGE` setting to use a modified version of `ManifestStaticFilesStorage` with `max_post_process_passes` set to 0, and runs the `collectstatic` command. If the issue described (raising `UnboundLocalError` due to `substitutions` variable being referenced before assignment) occurs, the script prints the stack trace and exits with code 0, indicating the issue is present as expected. If the error does not occur (meaning the issue is fixed or otherwise does not manifest), it raises an `AssertionError`.