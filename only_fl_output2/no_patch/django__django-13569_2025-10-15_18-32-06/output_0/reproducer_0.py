# reproducer.py
import os
import sys

import django
from django.conf import settings
from django.db import models
from django.db.models import Count

# Configuring Django settings (minimal configuration)
SETTINGS_DICT = {
    'INSTALLED_APPS': ['__main__'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    }
}

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

def main():
    settings.configure(**SETTINGS_DICT)
    django.setup()

    # Defining models inline
    class Thing(models.Model):
        pass

    class Related(models.Model):
        thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name='related')

    # Creating tables
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Thing)
        schema_editor.create_model(Related)

    # Populating the database
    t = Thing.objects.create()
    rs = [Related.objects.create(thing=t) for _ in range(2)]

    try:
        # The expected result should be a single group with `rc` = 2
        grouped_result = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')
        assert grouped_result.count() == 1 and grouped_result.first()['rc'] == 2, "Aggregation failed with `order_by('?')`"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error if assertion fails
    else:
        print("Issue fixed.")
        sys.exit(0)  # Exit without error if assertion passes

if __name__ == "__main__":
    main()
