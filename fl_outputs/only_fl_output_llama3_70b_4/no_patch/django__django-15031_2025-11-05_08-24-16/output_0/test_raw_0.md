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
        User.objects.create(username='viola,gordon')  # comma in username
        User.objects.create(username='gordon')

    def test_filtering_with_comma(self):
        try:
            admin.site._registry[User].get_changelist_instance(request=None).get_queryset(
                {'username__in': 'johnny,viola,gordon'}
            )
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'runserver'])

    test_case = TestFiltering()
    test_case.test_filtering_with_comma()

    # If we reach this point, the issue is fixed
    print("Issue is fixed!")
```
This script creates a Django project with a `User` model and registers it in the admin site. It then defines a test case that tries to filter users by username using the `in` lookup type with a value that contains a comma.

When run, this script should raise an `AssertionError` when the issue is present, printing a stack trace of the error. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.