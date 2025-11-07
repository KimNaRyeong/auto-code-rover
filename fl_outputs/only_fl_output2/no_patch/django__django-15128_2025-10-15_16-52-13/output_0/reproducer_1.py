# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Q

# Function to print stack trace
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else 'Unknown'
        print(f'  File "{frame.filename}"', line_number, f": {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Define the Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),  # Use current file as the app
)

# Monkey patching the app registry to accept our main script as an app
django.apps.AppConfig.__name__ = "AppConfig"
django.apps.AppConfig.label = 'main'
django.apps.AppConfig.path = os.path.dirname(os.path.abspath(__file__))

# Required for Django to setup models
django.setup()

# Define models
class Foo(models.Model):
    qux = models.ForeignKey("Qux", on_delete=models.CASCADE, related_name="foos")

class Bar(models.Model):
    foo = models.ForeignKey("Foo", on_delete=models.CASCADE, related_name="bars")
    another_foo = models.ForeignKey("Foo", on_delete=models.CASCADE, related_name="other_bars")
    baz = models.ForeignKey("Baz", on_delete=models.CASCADE, related_name="bars")

class Baz(models.Model):
    pass

class Qux(models.Model):
    bazes = models.ManyToManyField("Baz", related_name="quxes")

# Simulate database table creation
models.Model.check = classmethod(lambda cls, **kwargs: None)
try:
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Foo)
        schema_editor.create_model(Bar)
        schema_editor.create_model(Baz)
        schema_editor.create_model(Qux)
except Exception as e:
    print("Failed to create model tables:", e)
    os._exit(1)

# Reproduce the issue
try:
    qux = Qux.objects.create()
    Baz.objects.create()  # Ensure there's at least one Baz to avoid empty queryset operations
    qs1 = qux.foos.all()
    qs2 = Foo.objects.filter(
        Q(bars__baz__in=qux.bazes.all()) | Q(other_bars__baz__in=qux.bazes.all())
    )
    # This sequence raises AssertionError
    result = qs1 | qs2
    print("No AssertionError, script executed successfully.")
except AssertionError as e:
    print_stacktrace(e)
    os._exit(1)  # Indicates failure to handle the issue due to AssertionError
except Exception as e:
    print("Unexpected error:", str(e))
    os._exit(2)  # Handles unexpected errors
else:
    os._exit(0)  # Indicates success, no issues encountered
