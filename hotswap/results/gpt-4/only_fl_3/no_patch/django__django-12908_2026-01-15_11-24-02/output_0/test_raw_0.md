```python
# reproducer.py

import os
import django
from django.db import models
from django.db.models import Value, IntegerField
from django.conf import settings
from django.core.management import execute_from_command_line

# Configuration for a minimal Django project
settings.configure(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "__main__",  # This script is the main application
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    },
    USE_TZ=True,
)

django.setup()

# Define models
class User(models.Model):
    username = models.CharField(max_length=128)

    @classmethod
    def get_or_create_admin_user(cls):
        return cls.objects.get_or_create(username="admin")[0]


class Sample(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Testing function
def test_union_annotated_diff_distinct():
    # Utility to print stack trace
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

    try:
        # Setup
        user = User.get_or_create_admin_user()
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
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
        assert qs.count() == 2, "Distinct after union does not work as expected."

    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    # Run migrations
    execute_from_command_line([os.path.abspath(__file__), "migrate"])

    # Execute test
    test_union_annotated_diff_distinct()
```

This standalone Python file acts as its own Django project, creating a minimalistic setup to reproduce the database issue. When executed, it will attempt to validate the distinct operation after a queryset union with annotations, expecting it to work as presumed. If the issue is present, an `AssertionError` will be clearly logged along with a stack trace pointing out the exact failure point in the script. Please ensure Django is installed in your environment before running this script by using `pip install django`.