Here is the reproducer script:

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
    admin.autodiscover()
    class ClientAdmin(admin.ModelAdmin):
        search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

    client_qs = Client.objects.all()

    query = "test search query"
    for word in query.split():
        client_qs = client_qs.filter(Q(name__icontains=word) | Q(name2__icontains=word) | Q(contact_person__icontains=word) | Q(clientoffice__name__icontains=word) | Q(clientoffice__name2__icontains=word))

    try:
        list(client_qs)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

Please replace `'yourapp'` with your actual app name in the `from yourapp.models import Client, ClientOffice` line.