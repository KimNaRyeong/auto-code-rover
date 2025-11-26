I apologize for the previous mistake. Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django import forms

settings.configure(
    DEBUG=True,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.admin', 'reproducer_app'),
)

class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = ArrayField(
        models.CharField(max_length=42),
        default=list,
    )

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

def test_issue():
    setup_test_environment()
    from django.contrib.admin import site
    site._registry = {}

    class RelatedModelForm(forms.ModelForm):
        def clean(self):
            raise ValueError("whatever")

    class RelatedModelInline(admin.TabularInline):
        model = RelatedModel
        form = RelatedModelForm
        extra = 1

    @admin.register(Thing)
    class ThingAdmin(admin.ModelAdmin):
        inlines = [RelatedModelInline]

    request_factory = RequestFactory()
    request = request_factory.get('/admin/reproducer_app/thing/add/')
    request.user = 'admin'

    try:
        response = ThingAdmin(Thing, site).add_view(request)
        assert response.status_code == 200
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    # Simulate first submit with error
    data = {
        'relatedmodel_set-0-plop': ['test'],
        '_continue': 'Save and continue editing',
    }
    request = request_factory.post('/admin/reproducer_app/thing/add/', data)
    request.user = 'admin'

    try:
        response = ThingAdmin(Thing, site).add_view(request)
        assert response.status_code == 200
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    # Simulate second submit without error
    data = {
        'relatedmodel_set-0-plop': [],
        '_continue': 'Save and continue editing',
    }
    request = request_factory.post('/admin/reproducer_app/thing/add/', data)
    request.user = 'admin'

    try:
        response = ThingAdmin(Thing, site).add_view(request)
        assert response.status_code == 200
        raise AssertionError("Issue is fixed")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    test_issue()
```
This script defines the models, forms, and admin classes as described in the issue. It then uses Django's testing framework to simulate a user submitting the form twice. If the `ValueError` exception is raised during either submit, it prints the stack trace using the provided function and exits with an error code. If the issue is fixed, it raises an `AssertionError`.

Please note that you need to create an app named `reproducer_app` in your Django project for this script to work. You can do this by running `python manage.py startapp reproducer_app` in your terminal.

To run this script, execute `python3 reproducer.py` in the root directory of your project.