To ensure the script works as expected without relying on an existing Django setup or settings module, I will incorporate minimal Django settings directly within the script. This approach enables the script to run independently, facilitating a reproducible issue demonstration. Please ensure Django is installed in your environment before executing this script. This script will configure Django to run in memory using SQLite, avoiding the need for an external database.

Here's a standalone `reproducer.py` script designed to reproduce the described issue:

```python
# reproducer.py
import sys

from django.conf import settings
from django.core.management import execute_from_command_line

# Configure Django settings in-memory for the standalone script
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',  # Allows us to define models in this script
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_I18N=False,
    USE_L10N=False,
    USE_TZ=False,
)

# Import Django models and forms after configuring settings
from django.db import models
from django import forms

class MyModel(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        app_label = '__main__'

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield

class MyForm(forms.ModelForm):
    formfield_callback = all_required

    class Meta:
        model = MyModel
        fields = ['active', 'name']

def main():
    try:
        # Mimic Django's manage.py environment setup
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Use modelform_factory to create a form with a specific formfield_callback
        FactoryForm = forms.modelform_factory(MyModel, form=MyForm, formfield_callback=all_required)
        
        # Initialize the form and check assertions
        form = FactoryForm()
        assert form.fields['active'].required, "Field 'active' should be required."
        assert form.fields['name'].required, "Field 'name' should be required."
        print("Assertions passed. The issue might have been fixed.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
```

This script dynamically configures Django to facilitate a minimal running environment within a single file. It then attempts to define a model and a corresponding form using `modelform_factory` specifying a `formfield_callback` that should make all fields required. If fields are not required as expected, the assertion will fail, demonstrating the presence of the issue.

Ensure to run this script in an environment where Django is installed. You can do so by running `pip install Django` before executing the script with `python3 reproducer.py`.