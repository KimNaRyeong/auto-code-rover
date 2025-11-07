Here is the reproducer script:

```python
import django
from django.db import models

def model_to_dict(instance, fields=None):
    if fields and not isinstance(fields, (list, tuple)):
        raise TypeError("Fields must be a list or tuple")
    result = {}
    for f in instance._meta.get_fields():
        if fields is None or f.name in fields:
            if f.auto_created or f.many_to_one or f.many_to_many:
                value = model_to_dict(getattr(instance, f.name), fields)
                if value:
                    result[f.name] = value
            else:
                value = getattr(instance, f.name)
                if not isinstance(value, (models.Model, models.Manager)):
                    result[f.name] = value
    return result

class MyModel(models.Model):
    pass

def main():
    try:
        model_to_dict(MyModel(), fields=[])
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace.