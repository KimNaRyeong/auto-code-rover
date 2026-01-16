Given the specific requirements to directly reproduce the issue within a standalone Python script and the challenges faced in the previous attempts, we'll aim to structure this attempt carefully to ensure it precisely replicates the reported Django issue while being self-contained and executable. We will incorporate an explicit `app_label` for our models to get around the problem of Django requiring models to be part of an installed app. Additionally, we'll simulate a minimal Django environment setup within the script itself to avoid external dependencies.

```python
"""
reproducer.py

This scripts is designed to reproduce an issue where `order_by()` on a parent model crashes when `Meta.ordering`
contains expressions and it's run outside the context of a regular Django project environment.
"""

import django
from django.conf import settings
from django.db import models
from django.apps import apps
from django.db.models import F

def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=[
            'reproducer_app',  # This app label is used for our dynamically created models
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    )
    django.setup()

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

def main():
    setup_django_environment()

    class Parent(models.Model):
        name = models.CharField(max_length=255)

        class Meta:
            app_label = 'reproducer_app'
            ordering = [F('name').asc()]

    class Child(Parent):
        extra_field = models.CharField(max_length=255)

        class Meta:
            app_label = 'reproducer_app'

    # Dynamically create tables for our models. In a regular Django project, this corresponds to applying migrations.
    apps.get_models()

    try:
        # Ensure tables exist
        with django.db.connection.schema_editor() as schema_editor:
            schema_editor.create_model(Parent)
            schema_editor.create_model(Child)

        # Attempt to query the Child model, which will raise an AssertionError if the issue is present.
        Child.objects.create(name='John Doe', extra_field='Data')
        results = Child.objects.all()
        assert results.exists(), "No objects found, there should be at least one Child object."

        print("Test passed, issue not found.")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

Please ensure you have Django installed in your environment by running `pip install django` before executing the script with `python3 reproducer.py`. 

This script initializes a minimal Django settings environment, defines two models to simulate the inheritance structure mentioned in the issue, and attempts to perform database operations that would trigger the bug if it exists. The use of `F('name').asc()` in the `Meta.ordering` is critical as it directly relates to the described issue.