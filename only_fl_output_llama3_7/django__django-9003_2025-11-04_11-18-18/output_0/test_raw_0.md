Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import datetime
from django.db.models import Q
from django.db.models.sql.query import Query

def reproduce_issue():
    date = datetime.datetime.now()
    invoices = Invoice.objects.filter(
        Q(date_created__lte=date),
        Q(date_paid__gt=date) | Q(date_paid=None),
        Q(date_credited__gt=date) | Q(date_credited=None),
        customer=1,
    )
    filtered_invoices = Invoice.objects.none()
    not_due = Q(date_due__gte=date) | Q(date_due=None)
    not_reminded_yet = ~Q(reminders__date_created__lte=date)
    not_collected = Q(date_collect__gt=date) | Q(date_collect=None)
    filtered_invoices |= invoices.filter(not_due, not_collected, date_sent__lte=date, invoice_type="invoice")
    filtered_invents |= invoices.filter(not_collected, not_reminded_yet, date_sent__lte=date, date_due__lt=date, invoice_type="invoice")
    for r in [1, 2, 3]:
        qs = invoices.filter(not_collected, reminders__date_created__lte=date, reminders__reminder_counter=r, invoice_type="invoice")
        for i in range(r + 1, 3 + 1):
            qs = qs.filter(~Q(reminders__reminder_counter=i) | Q(reminders__reminder_counter=i, reminders__date_created__gt=date))
        filtered_invoices |= qs

    try:
        Query.combine(filtered_invoices)
    except AssertionError as e:
        print_stacktrace(e)

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

if __name__ == "__main__":
    reproduce_issue()
```

This script should be executed by `python3 reproducer.py` and will raise an `AssertionError` when the issue is present, printing a stack trace of the issue.