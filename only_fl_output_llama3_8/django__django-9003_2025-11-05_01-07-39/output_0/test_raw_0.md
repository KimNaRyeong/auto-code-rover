Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import datetime
from django.db.models import Q
from django.db.models.sql.query import Query

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
    date = datetime.datetime.now()
    invoices = Q(date_created__lte=date, date_paid__gt=date) | Q(date_paid=None)
    filtered_invoices = Q()
    not_due = Q(date_due__gte=date) | Q(date_due=None)
    not_reminded_yet = ~Q(reminders__date_created__lte=date)
    not_collected = Q(date_collect__gt=date) | Q(date_collect=None)
    filtered_invoices |= invoices & (not_due & not_collected & Q(date_sent__lte=date, invoice_type="invoice"))
    filtered_invoices |= invoices & (not_collected & not_reminded_yet & Q(date_sent__lte=date, date_due__lt=date, invoice_type="invoice"))
    for r in [1, 2, 3]:
        qs = invoices & (not_collected & Q(reminders__date_created__lte=date, reminders__reminder_counter=r, invoice_type="invoice"))
        for i in range(r + 1, 4):
            qs &= ~Q(reminders__reminder_counter=i) | Q(reminders__reminder_counter=i, reminders__date_created__gt=date)
        filtered_invoices |= qs
    try:
        Query.combine(filtered_invoices)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by creating a complex query with many-to-many self-joins and ORs, similar to the original code. It then attempts to combine the query using `Query.combine()`, which should raise an `AssertionError` when the issue is present.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`. If the issue is present, the script will print a stack trace showing the line numbers of the statements that caused the error.