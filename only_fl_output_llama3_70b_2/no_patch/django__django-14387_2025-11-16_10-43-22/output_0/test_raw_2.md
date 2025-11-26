Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.db.models import Q

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
import django
django.setup()

# Define the model
class Buss(models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = [('jurisdiction', 'name')]

# Create the database tables
from django.core.management import call_command
call_command('makemigrations', 'reproducer')
call_command('migrate')

def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

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

def main():
    # Create some test data
    Buss.objects.bulk_create([
        Buss(jurisdiction='GB', name=f'Bus {i}') for i in range(8)
    ] + [
        Buss(jurisdiction='Universal', name=f'Bus {i}') for i in range(10)
    ] + [
        Buss(jurisdiction='Company', name=f'Bus {i}') for i in range(12)
    ])

    # Test the issue
    qs = jurisdiction_qs('GB')
    result_count = qs.filter(jurisdiction='GB').count()
    if result_count != 8:
        raise AssertionError(f"Expected 8, got {result_count}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script sets up a Django environment, defines the `Buss` model, creates the database tables, and then tests the `jurisdiction_qs` function. If the issue is present, it raises an `AssertionError` with a stack trace of the issue.

Please note that you need to create a `reproducer` directory in the same directory as this script, and inside it, create a `settings.py` file with the following content:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
INSTALLED_APPS = ['reproducer']
```
This will set up an in-memory SQLite database for testing.