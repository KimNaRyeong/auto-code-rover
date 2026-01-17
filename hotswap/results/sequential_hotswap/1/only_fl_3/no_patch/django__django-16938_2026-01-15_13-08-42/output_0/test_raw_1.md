```python
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line


settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=(
        "__main__",
    ),
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
    objects = TestTagManager()
    name = models.CharField(max_length=120)
    master = models.ForeignKey(TestTagMaster, on_delete=models.SET_NULL, null=True)


class Test(models.Model):
    name = models.CharField(max_length=120)
    tags = models.ManyToManyField(TestTag, blank=True)


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
    # Mimic the Django management command execution.
    argv = [sys.argv[0], "migrate"]
    execute_from_command_line(argv)

    # Set up data for testing.
    tag_master = TestTagMaster.objects.create(name="master")
    tag = TestTag.objects.create(name="tag", master=tag_master)
    test = Test.objects.create(name="test")
    test.tags.add(tag)
    test.save()

    from django.core import serializers
    try:
        # Attempt serialization, which should raise the issue.
        serializers.serialize("json", Test.objects.all())
        print("Serialization completed without issue.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

This code follows the Django conventions closely and integrates the necessary components to reproduce the serialization issue within a Django environment, running models in memory for easy isolation and debugging. If the serialization problem is present, the given `print_stacktrace` function will output the traceback to stderr, providing diagnostic insight into the error, and the script will exit with code 1 indicating a failure. If the issue has been fixed, it will print a message indicating successful serialization and exit normally.