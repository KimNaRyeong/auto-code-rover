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
    raise ValueError('Unsupported lookup type')

class TestFiltering(TestCase):
    def setUp(self):
        User.objects.create(username='johnny')
        User.objects.create(username='viola,gordon')  # username contains a comma
        User.objects.create(username='gordon')

    def test_filtering_with_comma(self):
        try:
            response = self.client.get('/admin/auth/user/?username__in=johnny,viola,gordon')
            self.assertContains(response, 'johnny')
            self.assertContains(response, 'viola,gordon')  # this should fail
        except AssertionError as e:
            print_stacktrace(e)
            raise

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
        raise SystemExit(1)  # exit with code 1 if the issue is present
```
This script creates a Django project, defines a `User` model, and registers it in the admin site. It then creates three users: one with username 'johnny', one with username 'viola,gordon' (which contains a comma), and one with username 'gordon'.

The script then tries to filter the users using the `in` lookup type with a value that contains a comma (`username__in=johnny,viola,gordon`). If the issue is present, this should raise an `AssertionError`, which will be caught and printed with a stack trace. The script will exit with code 1 if the issue is present.

If you run this script and the issue is fixed, it should exit with code 0.