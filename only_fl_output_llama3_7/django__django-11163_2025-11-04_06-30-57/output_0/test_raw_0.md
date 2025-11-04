Here is the reproducer script:

```python
import django
from django.db import models

def model_to_dict(instance, fields=None):
    if fields and not any(field.name in fields for field in instance._meta.get_fields()):
        return {}
    # Your code here
    pass

class MyModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

def main():
    try:
        model_to_dict(MyModel(), [])
        raise AssertionError("Expected an empty dict")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a Django project, defines a simple model `MyModel`, and then calls the `model_to_dict` function with an instance of `MyModel` and an empty list of fields. If the issue is present, it should raise an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.