Here is a standalone Python script `reproducer.py` to reproduce the issue:
```
import os
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)

def get_password_reset_token(user):
    return PasswordResetTokenGenerator().make_token(user)

def reproducer():
    user = CustomUser(email="foo@example.com")
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

if __name__ == "__main__":
    try:
        reproducer()
    except Exception as e:
        print_stacktrace(e)
        os._exit(1)  # Exit with code 1
```
This script creates a custom user model, requests a password reset, changes the email address, and then tries to use the old password reset token. If the token is accepted, it raises an `AssertionError`. If the token is correctly rejected, it prints a success message and exits with code 0.

Note that this script assumes you have Django installed and configured in your project. You may need to modify the script to match your specific project setup.