import sys

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

# Minimal Django environment setup for standalone scripts
import django
from django.conf import settings
from django.apps import apps
from django.db import models

settings.configure(
    INSTALLED_APPS=[
        '__main__',  # This script is the "app"
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # Using in-memory database
        },
    },
)

# Import Django forms after configuring settings to avoid setup issues
from django import forms

django.setup()

# Define the models and forms as per the issue description
class MyModel(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        app_label = '__main__'

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['active', 'name']
        formfield_callback = all_required

apps.populate(settings.INSTALLED_APPS)

def test_formfield_callback_usage():
    # The issue is here; we expect modelform_factory to respect the formfield_callback
    # But we're not setting it directly. It should come from MyForm.Meta
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)
    
    form_instance = FactoryForm()
    assert form_instance.fields['active'].required, "Field 'active' is not required but should be."
    assert form_instance.fields['name'].required, "Field 'name' is not required but should be."
    print("All fields are correctly marked as required.")

if __name__ == '__main__':
    try:
        test_formfield_callback_usage()
        sys.exit(0)  # Exit with code 0 when the issue is fixed
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Indicate failure/issue present
