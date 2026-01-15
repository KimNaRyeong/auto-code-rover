Creating a `reproducer.py` script that accurately manifests the issue, including ensuring it operates in a stand-alone fashion and uses the provided `print_stacktrace` function requires a bit of manipulation. In the scenario described, there are potential complexities around dynamically creating models and applying migrations which are not typically handled in a simple Python script run against an existing Django project. This version will attempt to create a minimal Django setup, create necessary objects, perform the query, and check for the expected failure.

```python
import django
from django.conf import settings
from django.db import models

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        '__main__',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
)

django.setup()

# Define models
class Buss(models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = [('jurisdiction', 'name')]

# Migrate
from django.core.management import call_command
call_command('migrate', '--noinput')

# Reproduce issue
from django.db.models import Q

def create_buss_instances():
    # Setup data: Adjust as necessary to create a relevant test scenario
    Buss.objects.create(jurisdiction='GB', name='Test GB 1')
    # Add more instances if necessary
    print("Buss instances created.")

def reproduce_issue():
    try:
        qs = Buss.objects.filter(jurisdiction='GB')
        universal_qs = Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
        combined_qs = qs | universal_qs
        gb_count = combined_qs.filter(jurisdiction='GB').count()
        
        # Expected behavior condition:
        assert gb_count == 1, f"Expected 1, got {gb_count}"
        
        print("Issue not found: The count maches expectation.")
    except AssertionError as e:
        print_stacktrace(e)
        
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

if __name__ == '__main__':
    create_buss_instances()
    reproduce_issue()
```

**Notes:**

1. This script is designed to be executed in an environment where Django is already installed, without needing an existing Django project or app.
2. It dynamically creates a Django app with a minimal configuration, defines the `Buss` model directly within the script, and uses an in-memory SQLite database for simplicity.
3. After applying migrations to create the required database table(s), it attempts to reproduce the described issue by manipulating the queryset and filtering based on the described logic.
4. The `assert` statement may need to be adjusted based on the specific problem and what the expected results should be when the issue is not occurring.
5. The script directly calls Django's management commands to handle database migration and setup, which is generally not required in a conventional Django project setup. This approach is specific to reproducing the issue in a standalone script.