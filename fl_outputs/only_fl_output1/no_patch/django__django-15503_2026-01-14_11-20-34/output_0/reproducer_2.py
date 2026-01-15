import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

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

# Configure settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

from django.db import models

class JsonFieldHasKeyTest(models.Model):
    data = models.JSONField()

    class Meta:
        app_label = '__main__'

def run_tests():
    from django.test import TestCase

    class JsonFieldHasKeyTestCase(TestCase):
        def setUp(self):
            JsonFieldHasKeyTest.objects.create(data={'foo': 'bar'})
            JsonFieldHasKeyTest.objects.create(data={'1111': 'bar'})

        def test_json_field_has_key(self):
            c1 = JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count()
            c2 = JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count()
            self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
            self.assertEqual(c2, 1, "Should have found 1 entry with key '1111'")

    # Running tests
    try:
        from django.test.runner import DiscoverRunner
        test_runner = DiscoverRunner()
        test_suite = test_runner.build_suite(test_labels=['__main__.JsonFieldHasKeyTestCase'])
        results = test_runner.run_suite(suite=test_suite)
        if results.failures or results.errors:
            raise AssertionError("Test failures or errors occurred.")
    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)  # Using os._exit(1) to ensure the script exits with an error status

if __name__ == '__main__':
    run_tests()
    print("Tests completed successfully.")
    os._exit(0)
