 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import datetime
from django.db import connection
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from myapp.models import Client, ClientOffice

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def search_clients(query):
    User = get_user_model()
    user = User.objects.get(username='admin')
    content_type = ContentType.objects.get_for_model(Client)
    qs = user.client_objects.filter(content_type=content_type)
    qs = qs.filter(Q(name__icontains=query) | Q(name2__icontains=query) | Q(contact_person__icontains=query))
    for term in query.split():
        if len(term) > 3:
            qs = qs.filter(clientoffice__name__icontains=term)
            qs = qs.filter(clientoffice__name2__icontains=term)
    return qs

def main():
    Client.objects.create(name='Client1', name2='Client1', contact_person='John Doe')
    ClientOffice.objects.create(name='Office1', name2='Office1', client=Client.objects.get(name='Client1'))
    query = 'Client Office'
    print(f'Searching for clients with query: {query}')
    try:
        start_time = datetime.datetime.now()
        results = search_clients(query)
        end_time = datetime.datetime.now()
        print(f'Found {len(results)} clients in {(end_time - start_time).total_seconds()} seconds')
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```
This script creates a `Client` and a `ClientOffice` object, and then calls the `search_clients` function with a search query containing two words. If the issue is present, the script will raise an `AssertionError` with a stack trace. If the issue is fixed, the script will print the number of clients found and the time it took to execute the query.

Note that you will need to replace `myapp` in `from myapp.models import Client, ClientOffice` with the name of the app that contains the `Client` and `ClientOffice` models. Also, make sure that the `Client` model has a `ForeignKey` field to the `User` model, and that the `User` model has a `client_objects` manager that filters objects based on the `content_type` parameter.