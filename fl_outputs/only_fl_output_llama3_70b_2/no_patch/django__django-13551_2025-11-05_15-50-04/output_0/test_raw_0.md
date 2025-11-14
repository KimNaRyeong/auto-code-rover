Here is the `reproducer.py` file to reproduce the issue:
```
import os
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.test import TestCase

class CustomUser(AbstractBaseUser):
    email = 'foo@example.com'

def get_password_reset_token(user):
    return PasswordResetTokenGenerator().make_token(user)

class ReproducerTestCase(TestCase):
    def test_password_reset_token_invalidation(self):
        user = CustomUser()
        original_email = user.email
        password_reset_token = get_password_reset_token(user)
        
        # Change the user's email address
        user.email = 'bar@example.com'
        user.save()

        # Try to use the old password reset token
        try:
            PasswordResetTokenGenerator().check_token(user, password_reset_token)
        except ValidationError as e:
            print_stacktrace(e)
            return  # Expected behavior: token is invalid

        # If we reach this point, it means the issue is present
        raise AssertionError("Password reset token was not invalidated after email change")

if __name__ == '__main__':
    try:
        ReproducerTestCase().test_password_reset_token_invalidation()
    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)  # Exit with code 1 to indicate failure
```
This script defines a custom user model `CustomUser` and a test case `ReproducerTestCase`. The test case creates a user, generates a password reset token, changes the user's email address, and then tries to use the old password reset token. If the token is not invalidated, it raises an `AssertionError`.

When run with `python3 reproducer.py`, this script will raise an `AssertionError` if the issue is present, printing a stack trace of the error. If the issue is fixed, the script will exit with code 0.