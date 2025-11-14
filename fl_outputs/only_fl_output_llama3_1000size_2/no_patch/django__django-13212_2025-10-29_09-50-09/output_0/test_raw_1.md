Here is the reproducer script:

```python
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def my_validator(value):
    if not value.endswith('@example.com'):
        raise ValidationError(_('Invalid email address %(value)s'), params={'value': value})

try:
    my_validator('test')
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script defines a custom validator `my_validator` that raises a `ValidationError` if the provided email address does not end with '@example.com'. The error message includes the value parameter.