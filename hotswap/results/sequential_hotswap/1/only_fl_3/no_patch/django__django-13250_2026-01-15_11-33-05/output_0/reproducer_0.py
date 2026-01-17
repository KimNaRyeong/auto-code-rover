# reproducer.py

import os
import sys
import django
from django.conf import settings
from django.db import models, migrations, connection
from django.db.models import JSONField

# Define a minimal Django configuration
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=['__main__'],
    SECRET_KEY='temporary-key',
)

django.setup()


# Define a minimal model with a JSONField
class TestModel(models.Model):
    data = JSONField()

    class Meta:
        app_label = '__main__'


def create_test_data():
    """Create test objects in the database."""
    TestModel.objects.bulk_create([
        TestModel(data={}),
        TestModel(data={'baz': {'a': 'b', 'c': 'd'}}),
        TestModel(data={'k': True, 'l': False}),
        TestModel(data={'d': ['e', {'f': 'g'}]}),
        TestModel(data={'n': [None]}),
        TestModel(data=[1, [2]]),
    ])


def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else 'Unknown'
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


# Main routine to create test data, run queries and verify the results
def main():
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestModel)
    
    create_test_data()

    test_cases = [
        ({}, 6),
        ({'baz': {'a': 'b', 'c': 'd'}}, 1),
        ({'baz': {'a': 'b'}}, 1),
        ({'k': True, 'l': False}, 1),
        ({'d': ['e', {'f': 'g'}]}, 1),
        ({'d': ['e']}, 1),
        ([1, [2]], 1),
        ([1], 1),
        ([[2]], 1),
    ]

    try:
        for filter_, expected_count in test_cases:
            actual_count = TestModel.objects.filter(data__contains=filter_).count()
            assert actual_count == expected_count, f"Test case {filter_} failed. Expected {expected_count}, got {actual_count}."

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("All test cases passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
