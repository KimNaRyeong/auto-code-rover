import os
import pickle
import django
from django.conf import settings
from django.db import models

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

# Django setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        '__main__',
    ],
    USE_TZ=True,
)

django.setup()

# Model definition
class ModelA(models.Model):
    value = models.CharField(max_length=12)

    class Meta:
        app_label = '__main__'

# Reproducing the issue
def reproduce_issue():
    try:
        ModelA.objects.create(value="Test")
        row = ModelA.objects.values_list('id', 'value', named=True).first()

        # The following line is expected to raise a PicklingError
        pickle.dumps(row)
        # If no exception is raised, the issue is considered to be fixed
        print("Issue seems to be fixed.")
        os._exit(0)  # Use os._exit to ensure a clean exit without raising SystemExit exception
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, pickle.PicklingError), "The issue is not reproduced; another exception occurred."

if __name__ == '__main__':
    reproduce_issue()
