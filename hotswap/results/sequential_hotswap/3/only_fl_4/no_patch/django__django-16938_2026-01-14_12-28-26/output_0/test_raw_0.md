```python
# reproducer.py

import os
import sys

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

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
    import django
    django.setup()

    from django.core import serializers
    from django.db import models
    from django.db.models import Manager

    class TestTagManager(Manager):
        def get_queryset(self):
            qs = super().get_queryset()
            qs = qs.select_related("master")  # follow master when retrieving object by default
            return qs

    class TestTagMaster(models.Model):
        name = models.CharField(max_length=120)

    class TestTag(models.Model):
        # default = Manager() # solution is to define custom default manager, which is used by RelatedManager
        objects = TestTagManager()
        name = models.CharField(max_length=120)
        master = models.ForeignKey(TestTagMaster, on_delete=models.SET_NULL, null=True)

    class Test(models.Model):
        name = models.CharField(max_length=120)
        tags = models.ManyToManyField(TestTag, blank=True)

    try:
        tag_master = TestTagMaster.objects.create(name="master")
        tag = TestTag.objects.create(name="tag", master=tag_master)
        test = Test.objects.create(name="test")
        test.tags.add(tag)
        test.save()
        
        # Attempt serialization which should cause an error if the issue is present.
        serializers.serialize("json", [test])
        assert False, "The issue seems to be fixed. No exception raised."

    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
This script should be executed in the root of a Django project environment where the models and setup are appropriately configured in a Django application. Replace `'your_project.settings'` with the actual settings module of your Django project.

This script attempts to reproduce the issue described, and if the exception related to the serialization issue occurs, it will print a stack trace showing where the exception was raised, fulfilling the requirement to show the issue is present.

If the issue is fixed, the serialization process would complete successfully, and the assertion will trigger a message indicating that no exception related to the issue was raised.