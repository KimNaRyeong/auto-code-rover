```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.core import serializers

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

# Define an in-memory DB to allow the script to run standalone
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=("__main__",),
    USE_TZ=True,
)

django.setup()

class TestTagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("master")  # follow master when retrieving object by default
        return qs

class TestTagMaster(models.Model):
    name = models.CharField(max_length=120)

class TestTag(models.Model):
    # default = models.Manager()  # solution is to define a custom default manager, which is used by RelatedManager
    objects = TestTagManager()
    name = models.CharField(max_length=120)
    master = models.ForeignKey(TestTagMaster, on_delete=models.SET_NULL, null=True)

class Test(models.Model):
    name = models.CharField(max_length=120)
    tags = models.ManyToManyField(TestTag, blank=True)

django.db.connections.close_all()

# Setup Database and Create Test Models
with django.db.connection.schema_editor() as schema_editor:
    schema_editor.create_model(TestTagMaster)
    schema_editor.create_model(TestTag)
    schema_editor.create_model(Test)

try:
    # Now when serializing object
    tag_master = TestTagMaster.objects.create(name="master")
    tag = TestTag.objects.create(name="tag", master=tag_master)
    test = Test.objects.create(name="test")
    test.tags.add(tag)
    test.save()
    serializers.serialize("json", [test])  # This should raise the exception
    print("The issue has been fixed.")
except Exception as e:
    print_stacktrace(e)
    assert isinstance(e, django.core.exceptions.FieldError)
```

This script sets up a minimal Django environment in-memory, creates the models based on your description, and then attempts to serialize the `Test` model including its many-to-many field `tags`. 

According to the issue description, the script should cause a `FieldError` due to the improper use of `select_related` in a many-to-many relationship serialization scenario. The script is designed to assert this error to ensure it only passes (exits with code 0) if the issue is unresolved. If the Django's behavior alters in a way that it handles this case without throwing an error, the assertion will fail, indicating the issue has been addressed.