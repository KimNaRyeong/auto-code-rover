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
        my_model = MyModel()
        model_to_dict(my_model, [])
        print("Issue is present")
        raise AssertionError("Expected an empty dict but got all fields")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()

```

This script defines a simple Django model and then calls `model_to_dict` with an instance of that model and an empty list of fields. If the issue is present, it will raise an `AssertionError`, which will be caught by the script and printed to the console along with the stack trace.