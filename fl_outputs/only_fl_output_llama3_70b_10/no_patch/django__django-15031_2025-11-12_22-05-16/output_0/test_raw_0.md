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
    def test_filtering_with_comma(self):
        user1 = User(username='johnny')
        user2 = User(username='viola,foo')
        user3 = User(username='gordon')
        user1.save()
        user2.save()
        user3.save()

        try:
            admin.site._registry[User].get_changelist_instance(request=None).get_queryset(
                {'username__in': 'johnny,viola,foo,gordon'}
            )
            raise AssertionError("Expected LookupError or ValueError")
        except (LookupError, ValueError) as e:
            print_stacktrace(e)
            # If the issue is fixed, this exception should be raised
            assert False, "Expected LookupError or ValueError"

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    from django.core.management import execute_from_command_line

    execute_from_command_line(['', 'migrate'])
    TestFiltering().test_filtering_with_comma()
```
This script creates a Django project with a `User` model, registers it in the admin site, and then tries to filter users by username using the `in` lookup with values that contain commas. If the issue is present, an `AssertionError` will be raised, and if the issue is fixed, a `LookupError` or `ValueError` exception should be raised.

Please note that you need to create a `reproducer/settings.py` file in the same directory as this script, with the following content:
```
from django.conf import settings

settings.configure(
    INSTALLED_APPS=['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)
```