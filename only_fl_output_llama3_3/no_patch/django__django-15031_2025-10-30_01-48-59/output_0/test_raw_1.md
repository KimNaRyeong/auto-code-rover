Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    return value.replace(',', ' ')

try:
    from django.urls import path, include
    from django.conf import settings
    from django.test.utils import setup_test_environment

    setup_test_environment()
    settings.configure()

    User.objects.filter(username__in=['johnny,viola,gordon'])
except AssertionError as e:
    print_stacktrace(e)
    raise
```

This script will first set up the Django environment and configure the settings. Then it attempts to filter the `User` model by username using the `in` lookup with a value that contains a comma. If the issue is present, an `AssertionError` will be raised and caught, printing the stack trace before re-raising it.