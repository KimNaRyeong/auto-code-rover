```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

def setup_django_environment():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            '__main__',  # This module (reproducer.py) is considered an app by Django.
        ],
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
    )
    django.setup()

class Buss(models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = models.CharField(max_length=MAX_LENGTH)
    class Meta:
        unique_together = [('jurisdiction', 'name')]
        app_label = '__main__'  # Necessary for this stand-alone script to let Django know its app context.

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
    setup_django_environment()
    models.Model.check()

    # Dynamically create tables for our models
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Buss)

    # Add some test data
    Buss.objects.create(jurisdiction='GB', name='GB-Buss1')  # Pretend this adds a few more for various jurisdictions

    # Make our test query
    try:
        count = jurisdiction_qs('GB').filter(jurisdiction='GB').count()
        expected_count = 1  # Assuming there's only one Buss with jurisdiction 'GB'
        assert count == expected_count, f"Expected count to be {expected_count}, got {count}"
    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)  # Non-zero exit code to indicate failure
    else:
        print("Test passed: The filter chain works as expected.")

if __name__ == '__main__':
    main()
```