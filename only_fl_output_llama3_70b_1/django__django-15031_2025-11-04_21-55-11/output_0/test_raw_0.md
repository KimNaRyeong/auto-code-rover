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
        User.objects.create(username='viola,gordon')  # username contains a comma
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
    execute_from_command_line(['', 'test', '--verbosity', '0'])

```
This script defines a `User` model and registers it with the Django admin site. It then creates three users: one with username `'johnny'`, one with username `'viola,gordon'` (which contains a comma), and one with username `'gordon'`.

The `TestFiltering` test case attempts to filter the user list using the `username__in` lookup with a value that includes a comma. If the issue is present, this should raise an `AssertionError`. The script catches the exception, prints the stack trace using the provided function, and re-raises the exception.

If the issue is fixed, the test case will pass, and the script will exit with code 0.

To run the script, save it to a file named `reproducer.py` in the root directory of your Django project, and execute it with `python3 reproducer.py`.