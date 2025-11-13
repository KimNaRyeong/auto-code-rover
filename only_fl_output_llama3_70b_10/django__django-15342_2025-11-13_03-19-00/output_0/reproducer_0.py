import os
import sys
from django.db import models
from django.core.management import execute_from_command_line

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

# Create a Django project and app
os.system("django-admin startproject reproducer_project")
os.chdir("reproducer_project")
os.system("python manage.py startapp reproducer_app")

# Define a model with a field named _order
with open("reproducer_app/models.py", "w") as f:
    f.write("""
from django.db import models

class HistoricalRecord(models.Model):
    _order = models.IntegerField()
""")

try:
    # Run makemigrations to trigger the issue
    execute_from_command_line(["manage.py", "makemigrations", "--dry-run"])
except Exception as e:
    print_stacktrace(e)
    assert isinstance(e, KeyError) and str(e) == "'order_with_respect_to'"
else:
    sys.exit(0)
