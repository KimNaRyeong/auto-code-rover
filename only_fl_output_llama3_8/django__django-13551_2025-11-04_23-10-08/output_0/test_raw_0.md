Here is the `reproducer.py` file that reproduces the issue:

```python
import django
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.exceptions import ValidationError
from django.test.utils import CaptureStandardStreams
from django.test.client import RequestFactory
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class MyUser(AbstractBaseUser):
    email = 'foo@bar.com'

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

def main():
    request_factory = RequestFactory()
    request = request_factory.get('/')
    user = MyUser(email='foo@bar.com')
    user.set_password('password123')
    user.save()
    token_generator = PasswordResetTokenGenerator()

    # Create a password reset token
    token = token_generator.make_token(user)

    # Change the email address
    user.email = 'new_email@example.com'
    user.save()

    # Try to use the old password reset token
    try:
        token_generator.check_token(token)
        raise AssertionError("Password reset token should be rejected")
    except ValidationError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates a test user, generates a password reset token for that user, changes the email address of the user, and then tries to use the old password reset token. If the issue is present, it should raise an `AssertionError` with a stack trace showing the line numbers.