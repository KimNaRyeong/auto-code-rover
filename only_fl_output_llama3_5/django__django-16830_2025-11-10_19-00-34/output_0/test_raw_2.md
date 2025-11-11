Here is the reproducer script:

```python
import django
from django.db import models

django.setup()

class ParentModel(models.Model):
    id = models.BigIntegerField(primary_key=True)

class ChildModel(ParentModel):
    pass

def main():
    try:
        child_model = ChildModel(id=1)
        parent_model = ParentModel()
        parent_model.save(force_insert=False)  # Set force_insert to False
        child_model.save(force_insert=True)
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        assert False, "Expected AssertionError"

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines the `ParentModel` and `ChildModel`, and then attempts to save instances of both models with different values for the `force_insert` parameter. If the issue is present, it will print the stack trace and raise an `AssertionError`.