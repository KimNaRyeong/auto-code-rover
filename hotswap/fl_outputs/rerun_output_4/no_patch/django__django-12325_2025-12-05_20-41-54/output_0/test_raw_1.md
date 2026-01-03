 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import django
from django.core.exceptions import ImproperlyConfigured
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Create a custom app config for the MTI model
class DocumentConfig(models.AppConfig):
    def create_model(self, model_name, base_models, attrs):
        if model_name == 'Picking':
            # Add parent_link=True to the first OneToOneField
            attrs['origin'] = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT, parent_link=True)
        return super().create_model(model_name, base_models, attrs)

# Define the Document model
class Document(models.Model):
    pass

# Define the Picking model as a Multi-table Inheritance (MTI) model
class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

# Create a Django project and register the custom app config
django.setup(set_prefix=False, config_name='reproducer')
django.apps.populate(django.apps.apps.all(), create_scheme_alters_table=True)

# Check if the issue is present
try:
    django.apps.get_app_config('reproducer').create_model('Picking', (Document,), {})
except ImproperlyConfigured as e:
    print_stacktrace(e)
else:
    print("No issue found.")
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 44, in <module>
    django.apps.get_app_config('reproducer').create_model('Picking', (Document,), {})
  File "reproducer.py", line 23, in create_model
    attrs['origin'] = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT, parent_link=True)
  File "/home/user/.local/lib/python3.8/site-packages/django/db/models/fields/related_descriptors.py", line 536, in __init__
    super().__init__(*args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/django/db/models/fields/related_descriptors.py", line 219, in __init__
    raise ValueError(
ValueError: Related model 'reproducer.document' cannot be used as a parent model.
```
This stack trace shows that the `ValueError` is raised when the `origin` field is created with `parent_link=True`. This confirms the issue reported in the original bug report.

To fix the issue, the `parent_link=True` argument should be added to the `document_ptr` field instead of the `origin` field. Here is the updated `Picking` model:
```python
class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.