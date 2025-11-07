import django
from django.db import models

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
        django.setup()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Django setup failed"

    class MyModel(models.Model):
        pub_date = models.DateTimeField("date published")

    my_obj = MyModel(pub_date="2022-01-01")
    my_obj.save()

    # Change the publication date
    my_obj.pub_date = "2022-02-01"
    my_obj.save()

    # Get the history for the model
    try:
        from django.contrib.admin.models import LogEntry
        log_entries = LogEntry.objects.filter(content_type__app_label='my_app', object_id=my_obj.id)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Failed to get log entries"

    if not any("date published" in entry.change_message for entry in log_entries):
        raise AssertionError("Expected 'date published' in the change message")

if __name__ == "__main__":
    reproduce_issue()
