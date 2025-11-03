Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import django
from django.contrib import admin
from django.db.models import Q
from yourapp.models import Client, ClientOffice  # Replace 'yourapp' with your actual app name

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
    django.setup()
    admin.site.register(Client, ClientAdmin)
    
    client_qs = Client.objects.all()
    for query in ["word1 word2", "word3 word4"]:
        query_qs = client_qs.filter(Q(name__icontains=query) | Q(name2__icontains=query) | Q(contact_person__icontains=query) | Q(clientoffice__name__icontains=query) | Q(clientoffice__name2__icontains=query))
        if query_qs.count() > 0:
            raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a Django project, registers the `Client` model with an admin interface, and then performs searches for clients using various query strings. If any of these queries return results, it raises an `AssertionError`, which is caught and printed to the console along with a stack trace.

To use this script, replace `'yourapp'` in the import statement with the name of your actual Django app. Then, run the script using `python3 reproducer.py`. If the issue is present, you should see an `AssertionError` message followed by a stack trace.