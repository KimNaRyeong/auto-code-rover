```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Value, IntegerField

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Minimal Django configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
)

django.setup()

# Models definition
class User(models.Model):
    username = models.CharField(max_length=150)

class Sample(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Functions
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

# Script
def main():
    # Setup
    User.objects.all().delete()
    Sample.objects.all().delete()
    user = User.objects.create(username='admin')

    Sample.objects.create(user=user, name="Sam1")
    Sample.objects.create(user=user, name="Sam2 acid")
    Sample.objects.create(user=user, name="Sam3")
    Sample.objects.create(user=user, name="Sam4 acid")
    Sample.objects.create(user=user, name="Dub")
    Sample.objects.create(user=user, name="Dub")
    Sample.objects.create(user=user, name="Dub")

    qs = Sample.objects.filter(user=user)
    qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
    qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))

    qs = qs1.union(qs2).order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK

    try:
        assert qs.count() == 2, "Distinct on name after union should return 2"
        print("Issue not present or already fixed.")
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```

This script sets up a minimal Django environment, defines the necessary models (User and Sample), and reproduces the issue as described. Upon running `python3 reproducer.py`, it attempts to demonstrate the problem with `.distinct()` not functioning as expected after `.union()` operation with annotated querysets. It will print a detailed stack trace if the assertion fails due to the presence of the issue.