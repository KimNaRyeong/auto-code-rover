Here is the reproducer script:

```python
import os
import django
from django.contrib.auth.models import UserManager, User
from django.core.exceptions import AuthenticationFailed
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    
    backend = ModelBackend()
    try:
        user = User.objects.create(username='testuser')
        backend.authenticate(None, username=None, password=None)
    except AuthenticationFailed as e:
        print_stacktrace(e)
        raise AssertionError("Expected the script to fail")

if __name__ == "__main__":
    main()

class ModelBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserManager().get_user_model().USERNAME_FIELD)
        try:
            user = UserManager().get_by_natural_key(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserManager().set_password(password)
        else:
            ...
```

This script sets up a Django environment, defines a `ModelBackend` class that reproduces the issue, and then attempts to authenticate with a username of `None`. If the authentication fails (which it should), it prints the stack trace and raises an `AssertionError`.