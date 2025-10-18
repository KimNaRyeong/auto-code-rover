import os
import django
from django.conf import settings
from django.db import models
import pickle

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

# Setting up Django without an actual project
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    SECRET_KEY='abcde12345',
)

django.setup()

# Define a simple model
class ModelA(models.Model):
    value = models.CharField(max_length=12)

    class Meta:
        app_label = '__main__'

# Create the tables
try:
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(ModelA)
except django.db.utils.OperationalError:
    # Assuming the table already exists
    pass

# Create a test instance
ModelA.objects.create(value='test value')

try:
    # Query the instance
    row = ModelA.objects.values_list('id', 'value', named=True).first()

    # Trying to pickle the Row instance
    _ = pickle.dumps(row)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue with pickling django.db.models.query.Row detected.") from e
else:
    print("Row object pickled successfully. No issue detected.")

