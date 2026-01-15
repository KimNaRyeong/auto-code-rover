```python
import os
import django
from django.conf import settings
from django.db import models as db_models

# Setup Django project environment
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
    INSTALLED_APPS=('__main__',),
    SECRET_KEY='asdv234234^&*^&*dfgdfg',
    ALLOWED_HOSTS=[],
)

django.setup()

class Buss(db_models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = db_models.CharField(max_length=MAX_LENGTH)
    
    class Meta:
        unique_together = [('jurisdiction', 'name')]
        app_label = '__main__'

def jurisdiction_qs(for_jurisdiction):
    # Get busses identified by for_jurisdiction, and add other busses from 'Universal' and 'Company' where they don't clash.
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

if __name__ == '__main__':
    # Create tables for our models
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Buss)

    # Populating test data
    Buss.objects.create(jurisdiction='GB', name='Buss1')
    Buss.objects.create(jurisdiction='Universal', name='Buss2')
    Buss.objects.create(jurisdiction='Company', name='Buss3')
    
    try:
        # Applying test filters
        original_count = jurisdiction_qs('GB').count()
        filtered_count = jurisdiction_qs('GB').filter(jurisdiction='GB').count()
        
        assert original_count != filtered_count, 'Filtered count matches original count but should not!'
        print("No issue found.")
        
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    
    except Exception as e:
        print_stacktrace(e)
```