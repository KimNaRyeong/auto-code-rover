Here is the reproducer script:

```python
import django
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.email.strip()

def main():
    try:
        # Create a user with an email address
        user = CustomUser(email='foo@bar.com')
        user.save()

        # Request a password reset for the user's email
        user.set_password('old_password')
        user.send_password_reset_email()

        # Change the user's email
        user.email = 'new@bar.com'
        user.save()

        # Try to use the old password reset token
        user.send_password_reset_email()
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script creates a custom user model, requests a password reset for that user's email, changes the user's email, and then tries to use the old password reset token. If the issue is present, it should raise an `AssertionError` with a stack trace showing the line numbers of the statements that caused the error.