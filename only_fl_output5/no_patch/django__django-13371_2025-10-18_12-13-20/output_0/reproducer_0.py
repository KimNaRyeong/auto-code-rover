import os
import sys
import django
import pickle
from django.conf import settings
from django.db import models


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


# Django setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        __name__,
    ],
    SECRET_KEY='abcde12345',
)

django.setup()

# Model definition
class ModelA(models.Model):
    value = models.CharField(max_length=12)

    class Meta:
        app_label = __name__


# Reproduce the issue
def reproduce_issue():
    try:
        # Create a test instance
        ModelA.objects.create(value='test')
        
        # Fetch the instance as a named Row
        row = ModelA.objects.values_list('id', 'value', named=True).first()

        # Attempt to pickle the Row instance
        pickle.dumps(row)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to pickle django.db.models.query.Row instance") from e
    else:
        print("Issue is fixed. Row object is pickleable.")


if __name__ == '__main__':
    reproduce_issue()
