```python
# reproducer.py
import os
import sys
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

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

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

def main():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.staticfiles',
        ],
        STATIC_URL='/static/',
        STATIC_ROOT='./staticfiles',
        STATICFILES_STORAGE='__main__.MyManifestStaticFilesStorage'
    )

    # Ensure the STATIC_ROOT directory is clean
    if os.path.exists(settings.STATIC_ROOT):
        for filename in os.listdir(settings.STATIC_ROOT):
            file_path = os.path.join(settings.STATIC_ROOT, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
                sys.exit(1)

    try:
        call_command('collectstatic', interactive=False, verbosity=0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present") from e

    print("The issue is fixed.")
    sys.exit(0)

if __name__ == '__main__':
    try:
        import django
        django.setup()
        main()
    except AssertionError as e:
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```