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
    from django.contrib.admin.util import prepare_lookup_value as original_prepare_lookup_value
    return original_prepare_lookup_value(lookup_type, value)

class TestFiltering(TestCase):
    def setUp(self):
        User.objects.create(username='johnny')
        User.objects.create(username='viola,gordon')  # username contains a comma

    def test_filtering_with_comma(self):
        try:
            admin.site._registry[User].get_changelist_instance(request=None).get_queryset(
                {'username__in': 'johnny,viola,gordon'}
            )
            self.fail("Expected LookupError")
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Filtering with comma in value is not supported")

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    from django.core.management import execute_from_command_line

    execute_from_command_line(['', 'migrate'])
    execute_from_command_line(['', 'test'])

```
This script creates a Django project with a `User` model, registers it in the admin site, and defines a test case that tries to filter users by username using the `__in` lookup with a value that contains a comma. If the filtering is successful, the test will fail with an `AssertionError`. If the filtering raises an exception (which should be a `LookupError`), the script will print the stack trace of the exception and raise an `AssertionError`.

To run this script, create a new Django project, add the `reproducer.py` file to the root directory of the project, and execute it with `python3 reproducer.py`.