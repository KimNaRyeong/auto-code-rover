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
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        __name__,  # Allow Django to detect this as an app
    ],
    USE_TZ=True,
)

django.setup()

class Sample(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        app_label = __name__

# Setup for reproducing the issue
from django.contrib.auth.models import User
from django.db.models import F

def setup_database():
    User.objects.all().delete()
    Sample.objects.all().delete()
    user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
    Sample.objects.create(user=user, name="Sam1")
    Sample.objects.create(user=user, name="Sam2 acid")
    Sample.objects.create(user=user, name="Sam3")
    Sample.objects.create(user=user, name="Sam4 acid")
    Sample.objects.create(user=user, name="Dub")
    Sample.objects.create(user=user, name="Dub")
    Sample.objects.create(user=user, name="Dub")

def reproduce_issue():
    user = User.objects.all().first()
    qs = Sample.objects.filter(user=user)
    qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
    qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
    qs = qs1.union(qs2)
    qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
    return qs.count()

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
    setup_database()

    try:
        count = reproduce_issue()
        assert count == 2, f"Expected count to be 2, got {count} instead."
        print("Issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code to indicate failure

    exit(0)  # Exit with success code
```