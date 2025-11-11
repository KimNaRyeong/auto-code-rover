import django
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.utils import IntegrityError
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

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

class ReproducerTestCase(TestCase):
    def test_reproducer(self):
        class MyModel(models.Model):
            name = models.CharField(max_length=255, unique=True)
            weight = models.IntegerField()

        try:
            my_model = MyModel(name='test', weight=1)
            UniqueConstraint(fields=['name'], name='name_unq_covering', include=['weight']).create_constraint(my_model._meta)
        except ImproperlyConfigured as e:
            print_stacktrace(e)
            raise AssertionError("Expected no error")

if __name__ == "__main__":
    try:
        django.setup()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected no error")
    test_result = ReproducerTestCase().run()
    if test_result.wasSuccessful():
        exit(0)
    else:
        exit(1)

