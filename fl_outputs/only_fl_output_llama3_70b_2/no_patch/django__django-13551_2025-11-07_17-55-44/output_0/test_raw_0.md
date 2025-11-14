Here is the `reproducer.py` file to reproduce the issue:
```
import os
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)

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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import django
    django.setup()

    user = CustomUser(email='foo@example.com')
    user.set_password('password')
    user.save()

    token_generator = PasswordResetTokenGenerator()
    password_reset_token = token_generator.make_token(user)

    # Change the user's email address
    user.email = 'bar@example.com'
    user.save()

    try:
        # Try to use the old password reset token with the new email address
        token_generator.check_token(user, password_reset_token)
        raise AssertionError("Password reset token should be invalid")
    except ValidationError as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```
This script creates a custom user model with an email field, and then goes through the sequence of steps described in the issue:

1. Creates a user account with email `foo@example.com`.
2. Requests a password reset token for that email address.
3. Changes the user's email address to `bar@example.com`.
4. Tries to use the old password reset token with the new email address.

If the issue is present, the script will raise an `AssertionError` when trying to use the old password reset token with the new email address. If the issue is fixed, the script will exit with code 0.

Note that this script assumes you have a `reproducer.settings` file in the same directory, which defines the Django settings for this reproduction script. You may need to create this file and configure it accordingly.