# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

# Define a simple logging function to simulate the lazy load detection
def log_lazy_load(instance, attribute):
    original_getattribute = instance.__class__.__getattribute__

    def custom_getattribute(self, name):
        if name == attribute:
            raise AssertionError("Lazy load detected for attribute '{}'".format(name))
        return original_getattribute(self, name)

    instance.__class__.__getattribute__ = custom_getattribute

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

# Minimal configuration for a Django environment
settings.configure(
    DEBUG=False,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # Assumes this standalone script represents an app context
    ],
    USE_TZ=True,
)

django.setup()

# Define models inline to avoid app registry complications
class Parent(models.Model):
    name = models.CharField(max_length=255)

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

try:
    # Create tables dynamically if not already present
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Parent)
        schema_editor.create_model(Child)

    # The existing logic to simulate the issue
    parent = Parent(name='parent_object')
    child = Child(parent=parent)
    parent.save()
    
    log_lazy_load(child, 'parent')  # Attach a simple logger to detect undesired lazy load
    
    child.save()

    # Attempt to trigger lazy load which should now fail due to our log_lazy_load logic, if issue present
    _ = child.parent.name

    print("Issue not detected: possibly fixed.")
    os._exit(0)

except AssertionError as e:
    print("Issue detected:")
    print_stacktrace(e)
    os._exit(1)

except Exception as e:
    print("Unexpected exception occurred:")
    print_stacktrace(e)
    os._exit(2)
