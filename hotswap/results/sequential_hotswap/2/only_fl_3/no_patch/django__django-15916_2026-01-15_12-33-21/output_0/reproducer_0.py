import django
from django.conf import settings
from django.db import models
from django import forms

# Setup Django without an actual project
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # Allows us to define models in this script
    ]
)
django.setup()


# Model definition
class MyModel(models.Model):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)


# Function to be used as formfield_callback
def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield


# Our custom ModelForm with a formfield_callback in Meta
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['active', 'name']
        formfield_callback = all_required


# The function to print the stack trace
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


# Reproducer logic
try:
    # Creating a form using modelform_factory
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)
    
    # Checking if formfield_callback is applied correctly 
    test_form = FactoryForm()
    for field_name, field in test_form.fields.items():
        if not field.required:
            raise AssertionError(f"Field '{field_name}' is not required, but it should be.")

    print("Issue is fixed. Exiting with code 0.")
    exit(0)

except Exception as e:
    print_stacktrace(e)
    exit(1)
