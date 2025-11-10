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
        User.objects.create(username='viola,gordon')  # username with comma
        User.objects.create(username='gordon')

    def test_filtering_with_comma(self):
        try:
            admin.site.urls  # Ensure the admin site is set up
            response = self.client.get('/admin/auth/user/?username__in=johnny,viola,gordon')
            self.assertContains(response, 'johnny')
            self.assertContains(response, 'viola,gordon')  # This should fail due to the comma in the username
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'test', '--verbosity', '2'])

```
This script creates a Django project with a `User` model and registers it in the admin site. It then defines a test case that tries to filter users by username using the `in` lookup type, including a value with a comma (`viola,gordon`). If the filtering fails due to the comma, an `AssertionError` is raised, and the script prints the stack trace using the provided function.

To run this script, create a new Django project and add the `reproducer.py` file to its root directory. Then, execute the script with `python3 reproducer.py`. If the issue is present, the script should raise an `AssertionError` and print the stack trace. If the issue is fixed, the script should exit with code 0.