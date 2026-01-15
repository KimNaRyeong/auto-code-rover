```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core.exceptions import FieldError
from django.db import models

# Define settings for Django project (minimal configuration)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=(
        "__main__",  # this script is the app
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Models definition to replicate the issue
class TestTagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("master")
        return qs

class TestTagMaster(models.Model):
    name = models.CharField(max_length=120)

class TestTag(models.Model):
    objects = TestTagManager()
    name = models.CharField(max_length=120)
    master = models.ForeignKey(TestTagMaster, on_delete=models.SET_NULL, null=True)

class Test(models.Model):
    name = models.CharField(max_length=120)
    tags = models.ManyToManyField(TestTag, blank=True)

# Function to print stack trace
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

# Test function to trigger serialization and capture the issue
def test_serialization():
    from django.core import serializers
    
    tag_master = TestTagMaster.objects.create(name="master")
    tag = TestTag.objects.create(name="tag", master=tag_master)
    test = Test.objects.create(name="test")
    test.tags.add(tag)

    try:
        # The following line is expected to raise the FieldError exception because of the issue
        serializers.serialize("json", [test])
    except FieldError as e:
        print_stacktrace(e)
        raise AssertionError("Serialization with select_related in custom manager failed.") from e

    # If no exception, it means the issue is fixed or not present.
    print("Test passed: Serialization succeeded without errors.")

if __name__ == "__main__":
    try:
        test_serialization()
    except AssertionError as ae:
        print(ae)
        exit(1)  # Exit with a non-zero code to indicate the issue is present
    exit(0)  # Exit with code 0 to indicate the issue is not present or fixed.
```