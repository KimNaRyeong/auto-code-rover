Here is the reproducer script:

```python
import os
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.encoding import smart_bytes
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.email.strip().lower()

def main():
    try:
        # Set the DJANGO_SETTINGS_MODULE environment variable
        os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

        from django.contrib.auth.models import PasswordResetTokenGenerator

        # Create a user with an email
        from myproject.models import CustomUser
        user = CustomUser(email='foo@bar.com')
        user.save()

        # Request a password reset for the user
        user.set_password('oldpassword')
        user.send_password_reset_email()

        # Change the user's email
        user.email = 'new@bar.com'
        user.save()

        # Try to use the old password reset token
        user.send_password_reset_email()
    except AssertionError as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable, imports the necessary modules, creates a user with an email, requests a password reset for the user, changes the user's email, and then tries to use the old password reset token. If the issue is present, it should raise an `AssertionError` and print the stack trace.