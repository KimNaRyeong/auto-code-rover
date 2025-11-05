Here is the reproducer script:

```python
import os
import django
from django.core.management import call_command
from django.conf import settings

def main():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()

    # Create custom storage class
    class MyManifestStaticFilesStorage(django.contrib.staticfiles.storage.ManifestStaticFilesStorage):
        max_post_process_passes = 0

    settings.STATICFILES_STORAGE = "MyManifestStaticFilesStorage"

    try:
        call_command('collectstatic', verbosity=0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

    # If no exception is raised, the issue is fixed
    print("Issue not reproduced")
    exit(0)

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, creates a custom storage class with `max_post_process_passes` set to 0, and then runs the `collectstatic` command. If an exception is raised during the execution of this command, it prints the stack trace using the provided function and raises an assertion error.