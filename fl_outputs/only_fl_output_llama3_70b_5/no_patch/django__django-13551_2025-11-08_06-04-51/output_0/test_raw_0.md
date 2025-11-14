Here is the `reproducer.py` file to reproduce the issue:
```
import os
from django.contrib.auth.models import AbstractBaseUser, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)

class MyPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # This is the fix: add the user's email address to the hash value
        # return f"{user.pk}{user.password}{timestamp}{user.email}"
        return f"{user.pk}{user.password}{timestamp}"

class ReproduceTestCase(TestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)
        self.user = CustomUser.objects.create_user(email='foo@example.com', password='password')

    def test_password_reset_token_invalidation(self):
        # Create a password reset token for the original email
        token_generator = MyPasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)

        # Change the user's email address
        self.user.email = 'bar@example.com'
        self.user.save()

        # Try to use the old password reset token
        url = reverse('password_reset_confirm')
        data = {'token': token, 'email': 'foo@example.com'}
        response = self.client.post(url, data)

        try:
            # This should raise an AssertionError if the issue is present
            assert response.status_code == 403, "Password reset token was not invalidated"
        except AssertionError as e:
            print_stacktrace(e)
            raise SystemExit(1)  # Exit with code 1 to indicate failure

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    django.setup()
    ReproduceTestCase().test_password_reset_token_invalidation()
```
This script creates a custom user model and a custom password reset token generator. It then sets up a test case to reproduce the issue:

1. Create a user with an email address `foo@example.com`.
2. Generate a password reset token for that email.
3. Change the user's email address to `bar@example.com`.
4. Try to use the old password reset token.

If the issue is present, the script will raise an `AssertionError` and print a stack trace of the error. If the fix is applied (i.e., adding the user's email address to the hash value in `MyPasswordResetTokenGenerator._make_hash_value()`), the script will exit with code 0.

To run the script, save it as `reproducer.py` in the root directory of your Django project and execute it with `python3 reproducer.py`.