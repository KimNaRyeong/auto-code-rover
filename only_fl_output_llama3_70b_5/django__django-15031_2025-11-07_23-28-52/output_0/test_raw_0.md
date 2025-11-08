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
        user2 = User(username='viola, gordon')
        user3 = User(username='gordon')

        user1.save()
        user2.save()
        user3.save()

        try:
            admin.site._registry[User].get_changelist_instance(request=None).get_queryset(
                {'username__in': 'johnny,viola, gordon'}
            )
            raise AssertionError("Expected LookupError or ValueError")
        except (LookupError, ValueError) as e:
            print_stacktrace(e)
            # If the issue is fixed, this exception should be raised
            self.fail("Expected LookupError or ValueError")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
    import django
    django.setup()
    TestFiltering().test_filtering_with_comma()
```
This script creates a Django project with a `User` model and registers it in the admin site. It then creates three users: one with username `'johnny'`, one with username `'viola, gordon'`, and one with username `'gordon'`.

The test case tries to filter the users using the `username__in` lookup with a value that contains a comma (`'johnny,viola, gordon'`). If the issue is present, this should raise a `LookupError` or `ValueError`. The script catches these exceptions and prints the stack trace using the provided function. If the issue is fixed, the test case will fail with an `AssertionError`.

To run the script, create a new Django project and add the `reproducer.py` file to its root directory. Then, execute the script using `python3 reproducer.py`.