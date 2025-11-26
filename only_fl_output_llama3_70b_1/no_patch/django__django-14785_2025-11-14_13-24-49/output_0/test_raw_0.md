Here is the `reproducer.py` script to reproduce the issue:
```
import os
import sys
from django.db import models
from django.test.utils import setup_test_environment, teardown_test_environment

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import reproducer.settings

setup_test_environment()

from django.db import IntegrityError
from reproducer.models import MyModel

try:
    obj = MyModel.objects.create(value=float('nan'))
    obj.refresh_from_db()
except TypeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    sys.exit(0)

teardown_test_environment()
```
And here is the `reproducer/settings.py` file:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'reproducer.apps.ReproducerConfig'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

class ReproducerConfig:
    name = 'reproducer'
```
And here is the `reproducer/models.py` file:
```
from django.db import models

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)
```

To run the script, create a new Django project and app using the following commands:
```
django-admin startproject reproducer
cd reproducer
python manage.py startapp reproducer
```
Then, create the `reproducer.py`, `reproducer/settings.py`, and `reproducer/models.py` files in the root directory of the project.

Finally, run the script using `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` with a stack trace. If the issue is fixed, it should exit with code 0.