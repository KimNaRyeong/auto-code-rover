# reproducer.py
import os
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

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Check if Django is already set up
if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "temp_app",  # Assume temp_app is where your models will temporarily live
        ),
        TIME_ZONE="UTC",
    )

# Simulate creating a temporary Django app. Normally, you'd place your models in a proper Django app.
temp_app_dir = os.path.join(os.path.dirname(__file__), "temp_app")
if not os.path.exists(temp_app_dir):
    os.makedirs(temp_app_dir)

with open(os.path.join(temp_app_dir, "__init__.py"), "w") as init_file:
    pass

with open(os.path.join(temp_app_dir, "models.py"), "w") as models_file:
    models_file.write("""
from django.db import models

class Foo(models.Model):
    a = models.CharField(max_length=255)
    d = models.IntegerField()

class Bar(models.Model):
    a = models.ForeignKey(Foo, on_delete=models.CASCADE)
    b = models.CharField(max_length=255)
""")

django.setup()

# Generate and apply migrations
execute_from_command_line(['manage.py', 'makemigrations', 'temp_app'])
execute_from_command_line(['manage.py', 'migrate'])

# Import the temporarily created models
from temp_app.models import Foo, Bar

import copy

try:
    foo1 = Foo.objects.create(a='foo1', d=1)
    foo2 = Foo.objects.create(a='foo2', d=2)
    bar1 = Bar.objects.create(a=foo1, b='bar1')
    bar2 = copy.copy(bar1)
    bar2.pk = None
    bar2.a = foo2

    assert bar2.a == foo2
    assert bar2.a.id == bar2.a_id

    # The following should fail on Django >= 2.0 if the issue is present
    assert bar1.a == foo1
    assert bar1.a.id == bar1.a_id
    print("Test passed, no issue detected.")
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(2)

# Cleanup by removing the temp_app directory
import shutil
shutil.rmtree(temp_app_dir, ignore_errors=True)
