Here's a `reproducer.py` script designed to run at the root directory of a Django project to reproduce the specified issue with `fields.E305` being raised on `ManyToManyFields` with `related_name='+'` for models with the same name in different apps.

```python
import os
import django
from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.db import models

# Adjust the following paths as per your Django project structure.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

class BaseTestModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)

def create_model(app_label, model_name):
    class Meta:
        app_label = app_label
    
    attrs = {
        '__module__': 'reproducer',
        'Meta': Meta,
        'm2m_field': models.ManyToManyField(BaseTestModel, related_name='+'),
    }
    
    return type(model_name, (BaseTestModel,), attrs)

def register_models():
    app_labels = ['app1', 'app2']
    for app_label in app_labels:
        model = create_model(app_label, 'TestModel')
        models.register_model(app_label, model)


register_models()

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

def run_migrations():
    try:
        call_command('makemigrations', 'app1', 'app2', check=True)
        print("Issue is not present.")
    except SystemCheckError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    run_migrations()
```

Before you run this script, make sure to adjust the `'DJANGO_SETTINGS_MODULE'` setting to match the path to your project's settings module. Moreover, if your project apps' labels don't match `'app1'` and `'app2'`, you should change the `app_labels` list inside the `register_models` function accordingly.

The script dynamically creates two models with a `ManyToManyField` pointing to a base model using `related_name='+'`, which should reproduce the mentioned issue under circumstances where this configuration leads to an `AssertionError`. When the issue is fixed, the script should execute successfully without raising an error, indicating the absence of the issue.