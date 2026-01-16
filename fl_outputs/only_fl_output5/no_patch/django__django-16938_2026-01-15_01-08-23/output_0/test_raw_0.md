```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core import serializers
from django.db import models
from django.db.models.manager import Manager

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    INSTALLED_APPS=["__main__"],
    BASE_DIR=BASE_DIR,
    SECRET_KEY='dummy',
)

django.setup()


class TestTagManager(Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("master")  # follow master when retrieving object by default
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


def main():
    # Create the necessary tables
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestTagMaster)
        schema_editor.create_model(TestTag)
        schema_editor.create_model(Test)

    # Create instances to serialize
    tag_master = TestTagMaster.objects.create(name="master")
    tag = TestTag.objects.create(name="tag", master=tag_master)
    test = Test.objects.create(name="test")
    test.tags.add(tag)

    try:
        # This should either pass quietly or throw an exception to be caught below
        serialized_data = serializers.serialize("json", [test])
        # If no exception is raised, it means the issue is potentially fixed or not triggered
        print("Issue not reproduced, no FieldError encountered.")
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, django.core.exceptions.FieldError), "Unexpected exception type."
        print("Issue reproduced successfully.")

if __name__ == "__main__":
    main()
```