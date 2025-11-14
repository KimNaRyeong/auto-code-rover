Here is the reproducer script:

```python
import os
from django.db import models
from django.db.models import Exists, Q
from django.test import TestCase

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
from django.conf import settings

django.setup()

class MyModel(models.Model):
    name = models.CharField(max_length=255)

class TestReproducer(TestCase):

    def test_reproducer(self):
        try:
            qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')
            if not qs.query.where_clause:
                raise AssertionError("WHERE block is missing")
        except AssertionError as e:
            print_stacktrace(e)
            os._exit(1)

if __name__ == '__main__':
    settings.configure()
    TestReproducer().test_reproducer()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable and then imports Django. It also configures the settings before running the test case.