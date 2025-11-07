Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    return value.replace(',', ' ')

try:
    User.objects.filter(username__in=['johnny,viola,gordon'])
except AssertionError as e:
    print_stacktrace(e)
    raise
```

This script will attempt to filter the `User` model by username using the `in` lookup. The `prepare_lookup_value` function is called with a string value that contains a comma. If the issue is present, an `AssertionError` will be raised and caught, printing the stack trace before re-raising it.