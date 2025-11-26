Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db import models
from django.db.models import Value, IntegerField
from django.test import TestCase

# Create a sample model
class Sample(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class ReproducerTestCase(TestCase):
    def setUp(self):
        self.user = self.get_or_create_admin_user()
        Sample.objects.create(user=self.user, name="Sam1")
        Sample.objects.create(user=self.user, name="Sam2 acid")
        Sample.objects.create(user=self.user, name="Sam3")
        Sample.objects.create(user=self.user, name="Sam4 acid")
        Sample.objects.create(user=self.user, name="Dub")
        Sample.objects.create(user=self.user, name="Dub")
        Sample.objects.create(user=self.user, name="Dub")

    def test_union_annotated_diff_distinct(self):
        qs = Sample.objects.filter(user=self.user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
        try:
            self.assertEqual(qs.count(), 2)
        except AssertionError as e:
            print_stacktrace(e)
            raise

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

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(["reproducer", "test", "--verbosity", "2"])
```
This script creates a sample model, sets up some test data, and then runs a test case that reproduces the issue. If the issue is present, it will raise an `AssertionError` with a stack trace. If the issue is fixed, the script will exit with code 0.

Note: You'll need to create a `reproducer` Django project with a `settings.py` file and run this script from the root directory of the project using `python3 reproducer.py`.