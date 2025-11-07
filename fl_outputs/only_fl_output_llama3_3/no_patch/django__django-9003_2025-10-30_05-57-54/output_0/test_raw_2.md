Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
from django.db import models
from django.db.models import Q, ManyToManyField

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

class Invoice(models.Model):
    customer = models.ForeignKey("Customer")
    reminders = ManyToManyField("Invoice", related_name="reminded_set", blank=True)

def reproduce_issue():
    date = datetime.datetime.now()
    invoices = Invoice.objects.filter(
        Q(date_created__lte=date),
        Q(reminders__date_created__lt=date) | Q(reminders__date_created=None)
    )
    filtered_invoices = Invoice.objects.none()
    not_due = Q(date_created__gte=date) | Q(date_created=None)
    not_reminded_yet = ~Q(reminders__date_created__lte=date)
    filtered_invoices |= invoices.filter(not_due, not_reminded_yet, date_created__lte=date)
    for r in [1, 2]:
        qs = invoices.filter(not_reminded_yet, reminders__date_created__lt=date, reminders__reminder_counter=r)
        for i in range(r + 1):
            qs = qs.filter(~Q(reminders__reminder_counter=i) | Q(reminders__reminder_counter=i, reminders__date_created__gt=date))
        filtered_invoices |= qs

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script creates a simple Django model `Invoice` with a many-to-many relationship to itself, and then attempts to reproduce the issue by executing a query that involves self-joins and OR conditions. The `reproduce_issue()` function is wrapped in a try-except block, which catches any `AssertionError` exceptions raised during the execution of the query. If an exception is caught, it prints the stack trace using the provided `print_stacktrace()` function and exits with code 1. Otherwise, it prints a success message and exits with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it using `python3 reproducer.py`. If the issue is present, you should see an `AssertionError` exception raised, along with a stack trace that shows the line numbers and code context.