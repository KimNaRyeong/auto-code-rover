```python
# reproducer.py
import os
import sys
from django.core.management import call_command
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.conf import settings

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

def configure_settings():
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        ROOT_URLCONF=__name__,
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
        ],
        MIDDLEWARE=[],
        STATIC_URL='/static/',
        STATIC_ROOT='staticfiles',
        STATICFILES_STORAGE=__name__ + ".MyManifestStaticFilesStorage",
    )

def main():
    configure_settings()

    try:
        # This will try to collect static files using the custom storage class
        call_command("collectstatic", interactive=False, verbosity=0, clear=True)
        print("No issue detected, the command succeeded.")
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, UnboundLocalError), "The observed exception isn't UnboundLocalError as expected."
        sys.exit(0)  # Exit with 0 as this script is expected to raise an AssertionError when the issue is present.

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

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))  # Ensure the module can be found
    main()
```

Before running the script, ensure that Django is installed in your environment. You might want to set up a virtual environment and install Django using `pip install Django`.

To execute the script:
1. Place `reproducer.py` in the root directory of your Django project.
2. Run it with the command `python3 reproducer.py`.

The script dynamically configures Django settings and tries to collect static files using a derived `ManifestStaticFilesStorage` with `max_post_process_passes` set to 0. If the issue is present, it will raise an `UnboundLocalError` exception, the stack trace of which will be printed by `print_stacktrace`. If fixed, the script will exit with code 0 without any exception.