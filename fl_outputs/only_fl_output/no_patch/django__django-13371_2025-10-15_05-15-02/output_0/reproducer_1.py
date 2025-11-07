import sys
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
import pickle


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

# Minimal Django settings to bootstrap the environment
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=(
        'testapp',
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

# Dynamically create a new app and model
app_name = "testapp"

try:
    os.mkdir(app_name)
except FileExistsError:
    pass

with open(os.path.join(app_name, "__init__.py"), "w") as f:
    pass

with open(os.path.join(app_name, "models.py"), "w") as f:
    f.write("""
from django.db import models

class ModelA(models.Model):
    value = models.CharField(max_length=12)
    """)

django.setup()

# Now running the migrate command to create the database schema
execute_from_command_line(['manage.py', 'migrate'])

# Importing the model after setup
from testapp.models import ModelA
from django.db import models


def main():
    try:
        # Make sure there is a ModelA instance
        ModelA.objects.create(value='Test value')

        # Attempt to reproduce the reported issue
        row = ModelA.objects.values_list('id', 'value', named=True).first()
        pickle.dumps(row)  # This line is expected to raise an exception if the issue exists
        print("No issue detected. Object pickled successfully.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    main()
