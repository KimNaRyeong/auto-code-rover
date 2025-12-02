 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import django
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectstaticCommand
from django.core.exceptions import ImproperlyConfigured

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

class MyCollectstaticCommand(CollectstaticCommand):
    def handle(self, *args, **options):
        self.storage = MyManifestStaticFilesStorage()
        super().handle(*args, **options)

def main():
    try:
        settings_module = "settings"
        django.setup(set_prefix=False)
        django.conf.settings.configure(
            DEBUG=True,
            STATICFILES_STORAGE=MyManifestStaticFilesStorage,
            STATIC_URL="/static/",
            STATIC_ROOT="staticfiles",
        )

        command = MyCollectstaticCommand()
        command.handle(*args, **{})

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
The script sets up a Django project with the custom `MyManifestStaticFilesStorage` class and runs the `collectstatic` command. If `max_post_process_passes` is set to 0, the script will raise an `UnboundLocalError` and print a stack trace. If `max_post_process_passes` is set to a positive integer, the script will exit with code 0.