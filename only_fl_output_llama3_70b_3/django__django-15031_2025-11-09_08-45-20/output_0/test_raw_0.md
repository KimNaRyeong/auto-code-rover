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
    else:
        raise ValueError("Unsupported lookup type")

class TestFiltering(TestCase):
    def setUp(self):
        User.objects.create(username='johnny')
        User.objects.create(username='viola,gordon')  # comma in username
        User.objects.create(username='gordon')

    def test_filtering_with_comma(self):
        try:
            admin.site.urls  # Ensure the admin site is set up
            response = self.client.get('/admin/auth/user/?username__in=johnny,viola,gordon')
            self.assertContains(response, 'johnny')
            self.assertContains(response, 'viola,gordon')  # This should fail due to the comma in username
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'runserver'])

    test_case = TestFiltering()
    try:
        test_case.test_filtering_with_comma()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)  # Exit with code 1 if the issue is present
    else:
        print("Issue is fixed!")
```
This script creates a Django project, defines a `User` model, and registers it in the admin site. It then runs a test case that tries to filter users by username using the `in` lookup type with a value that contains a comma. If the issue is present, an `AssertionError` will be raised, and the script will print the stack trace and exit with code 1. If the issue is fixed, the script will print "Issue is fixed!" and exit with code 0.

Note that you'll need to create a `reproducer/settings.py` file with the necessary Django settings for this script to work. You can use the following minimal settings:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

SECRET_KEY = 'secret'
```