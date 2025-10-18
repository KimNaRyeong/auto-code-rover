# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models

# Minimal Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script is the app
    ],
    USE_TZ=True,
)

django.setup()

# Model Definitions
class ModelA(models.Model):
    pass


class ModelB(models.Model):
    pass


class ModelC(models.Model):
    model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)


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


# Main test
def main():
    # Ensuring the database tables are created
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(ModelA)
        schema_editor.create_model(ModelB)
        schema_editor.create_model(ModelC)

    # Reproducing the issue
    query_1 = ModelC.objects.select_related('model_a')
    query_2 = query_1.select_related('model_b')

    try:
        # Asserting the original QuerySet is not mutated (the issue)
        assert str(query_1.query) != str(query_2.query), "QuerySet mutation detected: The original QuerySet has been mutated."
        print("No issue detected, the original QuerySet and the new QuerySet are different as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with code 1 to indicate the issue is present

    # Clean up if necessary
    finally:
        try:
            os.remove('db.sqlite3')  # Clean up the database file
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    sys.exit(main())
