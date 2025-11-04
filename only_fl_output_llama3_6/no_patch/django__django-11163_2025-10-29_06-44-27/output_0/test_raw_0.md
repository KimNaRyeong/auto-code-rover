Here is the reproducer script:

```python
import django
from django.db import models

def model_to_dict(instance, fields=None):
    if fields and hasattr(instance, 'fields') and instance.fields:
        return {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name not in fields}
    else:
        return {}

class MyModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.CharField(max_length=255)

def main():
    try:
        model_to_dict(MyModel(), [])
        print("Issue is present")
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()
```

This script defines a `model_to_dict` function that mimics the behavior of Django's built-in `model_to_dict` function. It then creates a custom model and calls `model_to_dict` with an empty list of fields, which should raise an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the issue.