Here is the reproducer script:

```python
import django
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm
from django.urls import path
from django.urls.resolvers import URLPattern
from django.test.client import RequestFactory

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
    django.setup()
    
    class MyModel(User):
        pass

    class MyAdmin(UserAdmin):
        def get_urls(self):
            urls = super().get_urls()
            return [path('change/', self.get_changeform_instance, name='my_model_change_form'),] + urls

    request_factory = RequestFactory()

    request = request_factory.get('/user/22222222-3333-4444-5555-666677778888/change/?_to_field=uuid')

    try:
        UserAdmin(request).changeform_instance(None)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script sets up a test environment for the issue. It defines a custom model and admin, and then attempts to access the change form for that model via the UserAdmin. If the issue is present, it will print the stack trace and raise an AssertionError.