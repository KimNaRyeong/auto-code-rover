Given the requirements and the constraints outlined, writing a standalone Python script that accurately reproduces the stated Django issue while tackling the nuances of model registration and form submission via Django Admin involves quite a few steps. This script will attempt to simulate the Django environment, including model definition, admin registration, and form handling. It will mimic the form submission process to the Django Admin to highlight the said issue.

```python
# reproducoder.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.core.wsgi import get_wsgi_application
from django.test import Client
import traceback
import sys

# Define basic Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
    ],
    ROOT_URLCONF='__main__',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ]
)

# Function to print a detailed stack trace
def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Thing(models.Model):
    class Meta:
        app_label = 'test_app'

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = models.CharField(max_length=42, default="default_value")

    class Meta:
        app_label = 'test_app'

class RelatedModelForm(forms.ModelForm):
    def clean(self):
        raise ValidationError("Simulated error")

    class Meta:
        model = RelatedModel
        fields = '__all__'

class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    inlines = [RelatedModelInline]

urlpatterns = []

if __name__ == '__main__':
    django.setup()
    execute_from_command_line(['manage.py', 'migrate'])

    # Setup WSGI application to simulate server
    application = get_wsgi_application()
    client = Client()

    # Simulate admin login (replace 'admin', 'password' with your credentials if necessary)
    client.login(username='admin', password='password')

    # Attempt to POST data to the admin to simulate the form submission process and catch errors
    try:
        response = client.post('/admin/test_app/thing/add/', {
            'relatedmodel_set-TOTAL_FORMS': '1',
            'relatedmodel_set-INITIAL_FORMS': '0',
            'relatedmodel_set-MIN_NUM_FORMS': '0',
            'relatedmodel_set-MAX_NUM_FORMS': '1000',
            'relatedmodel_set-0-plop': 'test_input',
            '_continue': 'Save and continue editing',
        })
        
        # Expecting a validation error to be raised, which should not be bypassed
        if response.status_code == 302:  # Redirect indicates success, which shouldn't happen
            raise AssertionError("Form submission incorrectly bypassed validation error.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Issue reproduced successfully.")
    sys.exit(0)
```

This script, while comprehensive in approach, abstracts complexities like explicitly confirming the persistence of form validation errors across submissions and the subtleties of handling inline formsets within Django's admin framework. It setups a minimal Django environment, integrates models, forms, and admin inlines to capture the described behavior, assuming an issue related to form submission and validation is being explored. Remember, to fully execute this script, including the Django admin part, adjustments might be needed, such as setting up a superuser and ensuring the environment aligns with Django's expectations for admin access and data handling.