"""
reproducer.py
This script attempts to reproduce the issue where ordering by a query expression 
in a parent model's Meta class causes a crash.
"""

import os
import django
from django.conf import settings
from django.db import models
from django.apps import apps

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

def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=['__main__'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        SECRET_KEY='fake-key',
    )
    django.setup()
    apps.populate(settings.INSTALLED_APPS)

def create_models():
    class Parent(models.Model):
        name = models.CharField(max_length=255)

        class Meta:
            abstract = True
            ordering = [models.F('name').asc(nulls_last=True)]

    class Child(Parent):
        pass

    return Parent, Child

def main():
    setup_django_environment()
    Parent, Child = create_models()

    try:
        # Simulating operations that might reveal the issue.
        Child.objects.create(name="Alice")
        Child.objects.create(name="Bob")
        children = Child.objects.all()
        assert list(children), "Objects retrieval failed."

        print("Script executed successfully. Issue not found.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue has been reproduced.") from e

if __name__ == '__main__':
    main()
