Here is the reproducer script:

```python
import os
import django
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

django.setup()

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.email.strip()

def main():
    try:
        # Create a user with an email address
        from myapp.models import CustomUser
        user = CustomUser(email='foo@bar.com')
        user.save()

        # Request a password reset for the user's email
        user.set_password('old_password')
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        print(f"Password reset token: {token}")

        # Change the user's email
        user.email = 'new@bar.com'
        user.save()

        # Try to use the old password reset token
        token_generator = PasswordResetTokenGenerator()
        try:
            token_generator.check_token(token)
        except Exception as e:
            print_stacktrace(e)
            raise

    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()

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

```

This script creates a custom user model, requests a password reset for that user's email, changes the user's email, and then tries to use the old password reset token. If the issue is present, it should raise an `AssertionError` with a stack trace showing the line numbers of the statements that caused the error.