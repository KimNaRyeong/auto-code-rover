Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import django
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import AbstractBaseUser, User
from django.core.exceptions import ValidationError

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

# Set up Django
django.setup()

# Create a user with email address foo@example.com
user = User.objects.create_user('foo', 'foo@example.com', 'password')

# Request password reset for that email (unused)
token_generator = PasswordResetTokenGenerator()
token = token_generator.make_token(user)

# Change the user's email address
user.email = 'bar@example.com'
user.save()

# Try to use the password reset email with the old token
try:
    token_generator.check_token(user, token)
except ValidationError as e:
    print("Expected ValidationError not raised")
    print_stacktrace(e)
else:
    raise AssertionError("Password reset token should be rejected")

print("Issue reproduced successfully!")
```
This script creates a user with an email address, requests a password reset for that email, changes the user's email address, and then tries to use the password reset email with the old token. If the issue is present, it will raise an `AssertionError` when the token is accepted. If the issue is fixed, it will exit with code 0.

To run this script, save it as `reproducer.py` in the root directory of your Django project and execute it with `python3 reproducer.py`.