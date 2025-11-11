Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db.models import Q
from django.db import models

# Set up Django environment
django.setup()

class Client(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    contact_person = models.CharField(_('contact person'), max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))

admin.site.register(Client, admin.ModelAdmin)

# Set up search query
query = "word1 word2 word3"
qs = Client.objects.filter(Q(name__icontains=query) | Q(name2__icontains=query) | Q(contact_person__icontains=query))

try:
    # Try to execute the query
    list(qs)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
```

This script sets up a simple Django environment, defines the `Client` and `ClientOffice` models, registers the `Client` model with an admin interface, and then attempts to execute a search query that should trigger the unnecessary joins. If the issue is present, it will print the stack trace and raise an `AssertionError`.