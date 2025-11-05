Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import django
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import DateTimeField

# Set up Django project
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
django.setup()

from test_project.models import MyModel

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

def reproduce_issue():
    # Set up settings
    settings.TIME_ZONE = 'Europe/Paris'  # tz1
    settings.USE_TZ = True
    databases = {
        'legacy': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {'read_default_file': '....cnf'},
            'TIME_ZONE': 'Europe/Paris',  # tz2
        },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {'read_default_file': '....cnf'},
        }
    }

    # Create test data
    dt = make_aware(datetime(2017, 7, 6, 20, 50))
    MyModel.objects.create(my_datetime_field=dt)

    # Perform date lookup
    try:
        result = MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
        if not result:
            raise AssertionError("Date lookup failed")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a Django project, creates some test data, and then performs a date lookup using the `my_datetime_field` field. If the date lookup fails (i.e., no results are found), it raises an `AssertionError`, prints the stack trace, and exits with code 1.

Note that you'll need to create a `test_project` directory and add the necessary files (e.g., `settings.py`, `models.py`) for this script to work.