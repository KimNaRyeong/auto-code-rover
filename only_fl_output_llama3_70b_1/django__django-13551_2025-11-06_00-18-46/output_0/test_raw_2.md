Here is a revised standalone Python script `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

settings.configure(INSTALLED_APPS=['django.contrib.auth'], DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}})

def get_password_reset_token(user):
    return PasswordResetTokenGenerator().make_token(user)

def reproducer():
    user = User(email="foo@example.com")
    user.set_password("password")
    user.save()

    # Request password reset
    token = get_password_reset_token(user)
    print(f"Password reset token: {token}")

    # Change email address
    user.email = "bar@example.com"
    user.save()

    # Try to use the old password reset token
    try:
        PasswordResetTokenGenerator().check_token(user, token)
        raise AssertionError("Password reset token should be invalid")
    except ValueError:
        print("Password reset token is correctly rejected")

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

if __name__ == "__main__":
    setup_test_environment()
    try:
        reproducer()
    except Exception as e:
        print_stacktrace(e)
        os._exit(1)  # Exit with code 1
```
This script sets up a test environment, creates a user, requests a password reset, changes the email address, and then tries to use the old password reset token. If the token is accepted, it raises an `AssertionError`. If the token is correctly rejected, it prints a success message and exits with code 0.

Note that I added `DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}}` to the `settings.configure()` call to configure the database settings. This should fix the `ImproperlyConfigured` error you were seeing.