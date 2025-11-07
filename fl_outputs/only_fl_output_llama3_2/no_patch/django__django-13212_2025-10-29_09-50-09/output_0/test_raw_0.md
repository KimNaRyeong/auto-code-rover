Here is the reproducer script:

```python
def my_validator(value):
    if not value.endswith('@example.com'):
        raise ValidationError('Invalid email address', params={'value': value})

from django.core.exceptions import ValidationError

try:
    my_validator('test@example.com')
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script defines a custom validator `my_validator` that raises a `ValidationError` if the provided email address does not end with '@example.com'. The error message includes the value parameter.