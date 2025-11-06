Here is the reproducer script:

```python
import django
from django.db import models

def model_to_dict(instance, fields=None):
    if fields and hasattr(instance, 'field_names'):
        return {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name not in fields}
    else:
        return {}

class MyModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.CharField(max_length=255)

def main():
    try:
        django.setup()
        my_model = MyModel()
        result = model_to_dict(my_model, [])
        assert not result
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()

```

This script sets up the Django environment before calling the `model_to_dict` function. This should reproduce the issue you described.