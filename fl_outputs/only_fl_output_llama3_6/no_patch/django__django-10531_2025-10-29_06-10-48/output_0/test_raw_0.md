Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.test.utils import CaptureStandardOutput

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

def reproduce_issue():
    try:
        # Create a model
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        # Create an instance of the model
        obj = MyModel()

        # Change the publication date for the object
        obj.pub_date = "2022-01-01"

        # Save the changes
        obj.save()

        # Get the history entries
        content_type = ContentType.objects.get_for_model(MyModel)
        log_entries = LogEntry.objects.filter(content_type=content_type, action_flag=models.ACTION_UPDATE)

        # Check if the history entries contain verbose names
        for entry in log_entries:
            assert "date published" in str(entry.object_id), f"Expected 'date published' but got {entry.object_id}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a model, changes the publication date for an instance of that model, and then checks if the history entries contain verbose names. If they don't, it prints the stack trace and raises an `AssertionError`.