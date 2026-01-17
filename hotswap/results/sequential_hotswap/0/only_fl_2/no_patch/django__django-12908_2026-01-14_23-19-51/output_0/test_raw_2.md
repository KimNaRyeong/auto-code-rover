Let's create a `reproducer.py` script to reproduce the described issue accurately. This script will try to emulate the described scenario as closely as possible within a single standalone Python file, which includes setting up Django, creating models, and running the test case that covers the specific issue with union queryset and `.distinct()` not working as expected.

```python
# reproducer.py

import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Value, IntegerField

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY='please_dont_use_this_in_production',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',
    ),
    USE_TZ=True,
)

django.setup()

from django.contrib.auth.models import User


class Sample(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'


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


def run_test():
    from django.core.management import call_command
    from django.db.utils import OperationalError
    
    call_command('migrate')

    try:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        Sample.objects.bulk_create([
            Sample(user=user, name="Sam1"),
            Sample(user=user, name="Sam2 acid"),
            Sample(user=user, name="Sam3"),
            Sample(user=user, name="Sam4 acid"),
            Sample(user=user, name="Dub"),
            Sample(user=user, name="Dub"),
            Sample(user=user, name="Dub"),
        ])

        qs = Sample.objects.filter(user=user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs_union = qs1.union(qs2)
        qs_distinct = qs_union.order_by('name').distinct('name')

        assert qs_distinct.count() == 2, "Distinct on union queryset did not work as expected."
        print("Test passed: distinct() after union() works as expected.")
        
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    run_test()
```

This reproducer script sets up a minimal Django environment, creates a user and sample model instances, and attempts to query these models using `.union()` followed by `.distinct()` in a manner that is expected to fail under the conditions described in the issue. If it fails as expected due to the issue at hand, it will catch the assertion and print a detailed stack trace.

You can run this script directly with:

```bash
python3 reproducer.py
```

Please make sure you have Django installed in the Python environment where you execute this script. You can install Django with:

```bash
pip install Django
```

If the issue is present, it should raise the `AssertionError` as expected and print the stack trace. If the Django framework's behavior changes in the future to handle this case correctly, the test will pass, printing a success message without raising an exception.