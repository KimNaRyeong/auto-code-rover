Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import django
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.test.utils import override_settings

# Set up Django
django.setup()

class User(django.db.models.Model):
    email = django.db.models.EmailField(unique=True)

def get_password_reset_token(user):
    return PasswordResetTokenGenerator().make_token(user)

@override_settings(AUTH_USER_MODEL='__main__.User')
def test_password_reset_token():
    user = User(email='foo@example.com')
    user.save()

    # Request password reset
    token = get_password_reset_token(user)
    assert token is not None

    # Change email address
    user.email = 'bar@example.com'
    user.save()

    # Try to use old password reset token
    try:
        PasswordResetTokenGenerator().check_token(user, token)
    except ValidationError:
        print("Password reset token is correctly rejected")
        return 0

    raise AssertionError("Password reset token should be rejected")

if __name__ == '__main__':
    try:
        test_password_reset_token()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script defines a custom `User` model, sets up Django, and runs a test that reproduces the issue. If the issue is present, it raises an `AssertionError`. If the issue is fixed, it prints a success message and exits with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.