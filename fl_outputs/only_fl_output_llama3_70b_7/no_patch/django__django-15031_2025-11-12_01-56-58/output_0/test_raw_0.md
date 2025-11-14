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
    import reproducer.settings
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'runserver'])

    test_case = TestFiltering()
    test_case.test_filtering_with_comma()

    # If we reach this point, the issue is fixed
    print("Issue is fixed!")
```
This script sets up a Django project with a `User` model and registers it in the admin site. It then creates three users: one with username 'johnny', one with username 'viola,gordon' (which contains a comma), and one with username 'gordon'.

The test case tries to filter the users using the `in` lookup with a value that includes a comma (`username__in=johnny,viola,gordon`). If the issue is present, this should raise an `AssertionError`, which will be caught and printed with a stack trace. If the issue is fixed, the script will print "Issue is fixed!" and exit with code 0.

Note that you'll need to create a `reproducer` directory with a `settings.py` file containing the Django project settings for this script to work. You can use the following minimal `settings.py` file:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```