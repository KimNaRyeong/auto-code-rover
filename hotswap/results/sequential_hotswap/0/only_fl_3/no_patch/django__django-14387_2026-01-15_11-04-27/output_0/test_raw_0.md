```python
# reproducer.py
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

def setup():
    from django.conf import settings

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            '__main__',  # This script acts as the app
        ],
        USE_TZ=True,
    )

    import django
    django.setup()

    from django.db import models as db_models

    class Buss(db_models.Model):
        MAX_LENGTH = 25
        CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
        jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
        name = db_models.CharField(max_length=MAX_LENGTH)

        class Meta:
            unique_together = [('jurisdiction', 'name')]
            app_label = '__main__'

    return Buss

def populate_data(Buss):
    buss1 = Buss(jurisdiction='GB', name='Buss1')
    buss1.save()
    buss2 = Buss(jurisdiction='Universal', name='Buss2')
    buss2.save()
    buss3 = Buss(jurisdiction='Company', name='Buss3')
    buss3.save()

def jurisdiction_qs(Buss, for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

def reproduce_issue():
    try:
        Buss = setup()
        from django.db import migrations
        migrations.Migration.auto_created = True
        
        from django.core.management import call_command
        call_command('migrate', verbosity=0)

        populate_data(Buss)
        
        assert jurisdiction_qs(Buss, 'GB').filter(jurisdiction='GB').count() == 8, "Issue not reproduced - final filter is not breaking as expected."

    except AssertionError as e:
        raise e
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present, or the assertion condition is incorrect.")
        exit(0)
```

Note: 
- This script assumes you have Django installed and that you can execute scripts that utilize Django's ORM standalone. 
- You might need to adjust the assertion condition based on the actual data present in your model, as the hardcoded "8" in `assert` may not always match the expected scenario due to simplified setup and test data population.
- If you run this without the necessary Django setup, it will raise a configuration error. Ensure Django is properly installed and accessible within your environment.