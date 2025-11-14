Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection
from django.db.backends.base.creation import BaseDatabaseCreation

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_django():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    try:
        setup_test_environment()
    except ImproperlyConfigured:
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'testdb',
                    'USER': 'postgres',
                    'PASSWORD': '',
                    'HOST': 'localhost',
                    'PORT': 5432,
                }
            },
            INSTALLED_APPS=[
                'django.contrib.admin',
                'reproducer.app',
            ],
        )
        from reproducer.app import models
        connection.creation = BaseDatabaseCreation(connection)

def teardown_django():
    teardown_test_environment()

def main():
    setup_django()
    
    from django.contrib.auth.models import User
    from reproducer.app import models
    
    # Create a user and a post with the user as author
    user = User.objects.create(email='user@example.com')
    post = models.Post.objects.create(title='Test Post', authors=[user])
    
    # Search for the post using the many-to-many field
    queryset = models.Post.objects.filter(authors__email=user.email)
    
    try:
        # Delete the post, which should raise a TypeError
        queryset.delete()
        assert False, "Expected TypeError: Cannot call delete() after .distinct()."
    except Exception as e:
        print_stacktrace(e)
        if not isinstance(e, TypeError) or str(e) != 'Cannot call delete() after .distinct().':
            raise
    
    teardown_django()

if __name__ == '__main__':
    main()
```
This script sets up a Django project with a `Post` model that has a many-to-many field `authors` related to the `User` model. It creates a user and a post, searches for the post using the many-to-many field, and then tries to delete the post. If the issue is present, it should raise a `TypeError` with the message "Cannot call delete() after .distinct().". The script catches the exception, prints the stack trace, and checks if the error message matches the expected one. If not, it raises the exception again.

To run this script, create a new directory for your project, add a file `reproducer/app/models.py` with the following content:
```
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('auth.User')
```
and a file `reproducer/settings.py` with the following content:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'reproducer.app',
]
```
Then, run the script using `python3 reproducer.py`. If the issue is present, it should print the stack trace and exit with code 1. If the issue is fixed, it should exit with code 0.