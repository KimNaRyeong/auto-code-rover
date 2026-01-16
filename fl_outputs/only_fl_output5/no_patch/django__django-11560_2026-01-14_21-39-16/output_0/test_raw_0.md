```python
import os
import sys

# First, we need to set up a Django environment for the script to run.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer_settings')
try:
    import django
    django.setup()

    from django.db import models
    from django.db.models.functions import ExtractYear
    from django.core.management import call_command

    # Define a temporary Django settings module if it doesn't exist yet
    if not os.path.isfile('reproducer_settings.py'):
        with open('reproducer_settings.py', 'w') as f:
            f.write("""
SECRET_KEY = 'fake-key'
INSTALLED_APPS = ['__main__']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'reproducer_db.sqlite3',
    }
}
""")

    class MyModel(models.Model):
        duration = models.DurationField()

    # Print stack trace function as provided
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

    try:
        # Prepare the database
        call_command('makemigrations', '--no-input')
        call_command('migrate', '--no-input')

        # The actual test to reproduce the issue
        MyModel.objects.create(duration='1 00:00:00')  # 1 day
        try:
            annotated_qs = MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
            # We're forcing the query to be executed
            annotated_qs.first()
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced") from e

    except AssertionError as ae:
        print(ae)
        sys.exit(0)  # Means the issue is present as expected

    print("No issue found. Exiting without error.")
    sys.exit(0)

except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)
```