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

def test_model_to_dict():
    my_instance = MyModel()
    try:
        model_to_dict(my_instance, [])
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    test_model_to_dict()
```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`. If the issue is present, you should see an `AssertionError` raised with a stack trace.