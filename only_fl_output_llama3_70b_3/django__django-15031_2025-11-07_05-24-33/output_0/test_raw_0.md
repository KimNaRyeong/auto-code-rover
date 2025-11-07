Here is the `reproducer.py` file that reproduces the issue:
```
import os
from django.contrib import admin
from django.db import models
from django.test import TestCase

class User(models.Model):
    username = models.CharField(max_length=255)

admin.site.register(User)

def prepare_lookup_value(lookup_type, value):
    if lookup_type == 'in':
        return [x.strip() for x in value.split(',')]
    # ... other lookup types ...

class TestFiltering(TestCase):
    def setUp(self):
        User.objects.create(username='johnny')
        User.objects.create(username='viola,foo')
        User.objects.create(username='gordon')

    def test_filtering_with_comma(self):
        try:
            admin.site._registry[User].get_changelist_instance(request=None).get_queryset(
                {'username__in': 'johnny,viola,foo,gordon'}
            )
            raise AssertionError("Expected LookupError or ValueError")
        except (LookupError, ValueError) as e:
            print_stacktrace(e)
            # If the issue is fixed, this should not raise an exception
            self.fail("Expected no exception")

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    from django.core.management import execute_from_command_line

    execute_from_command_line(['', 'runserver'])

    test_case = TestFiltering()
    test_case.setUp()
    try:
        test_case.test_filtering_with_comma()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```
This script creates a Django project with a `User` model and registers it in the admin site. It then defines a test case that tries to filter users by username using the `in` lookup with a value that contains commas.

If the issue is present, the `prepare_lookup_value` function will raise a `LookupError` or `ValueError` when trying to split the value string. The script catches this exception and prints the stack trace using the provided `print_stacktrace` function.

If the issue is fixed, the test case should not raise an exception, and the script will exit with code 0.