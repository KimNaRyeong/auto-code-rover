# reproducerer.py

import os
import sys
from django.conf import settings
from django.core import serializers

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Setup minimal Django environment
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script will be recognized as an app, necessary for model discovery
    ),
    USE_TZ=True,
)

from django.db import models
from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

class TestTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("master")

class TestTagMaster(models.Model):
    name = models.CharField(max_length=120)

class TestTag(models.Model):
    master = models.ForeignKey(TestTagMaster, on_delete=models.SET_NULL, null=True, related_name="tags")
    name = models.CharField(max_length=120)
    objects = TestTagManager()

class Test(models.Model):
    name = models.CharField(max_length=120)
    tags = models.ManyToManyField(TestTag, blank=True)

# Dynamically create the database tables for defined models
from django.core.management import call_command
call_command('migrate')

try:
    tag_master = TestTagMaster.objects.create(name="master")
    tag = TestTag.objects.create(name="tag", master=tag_master)
    test = Test.objects.create(name="test")
    test.tags.add(tag)
    
    # Attempt serialization which should raise the described issue
    serialized_data = serializers.serialize("json", Test.objects.all())
    
    # If the serialization succeeds, we assume the issue is fixed/not present
    print("Serialization completed successfully, no error raised.")
    sys.exit(0)

except Exception as e:
    print_stacktrace(e)
    assert "cannot be both deferred and traversed using select_related at the same time" in str(e), "Unexpected error encountered."

if __name__ == "__main__":
    django.setup()
    main()
