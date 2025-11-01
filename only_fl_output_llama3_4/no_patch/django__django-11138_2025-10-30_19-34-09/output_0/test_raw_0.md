Here is the reproducer script:

```python
import os
import django
from django.db import models, connection
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

def reproduce_issue():
    settings_module = __import__('settings')
    settings = settings_module.settings

    # Set up the database
    connection.settings_dict['TIME_ZONE'] = 'Europe/Paris'
    connection.settings_dict['USE_TZ'] = True

    # Create a test model instance
    dt = make_aware(datetime(2017, 7, 6, 20, 50))
    MyModel.objects.create(my_datetime_field=dt)

    # Perform the date lookup
    result = MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()

    if not result:
        raise AssertionError("Date lookup failed")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a Django project, creates a test model instance with a datetime field, and then performs the date lookup. If the date lookup fails (i.e., no result is found), it raises an `AssertionError`. The script also prints the stack trace of the exception if one occurs.