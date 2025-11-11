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
        child_model.save(force_insert=True)
        query_set = ParentModel.objects.all()
        query_set.update(id=2)  # This should raise an AssertionError
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines the `ParentModel` and `ChildModel`, and then attempts to save an instance of `ChildModel` with the `force_insert=True`. After that, it updates all instances of `ParentModel` which should raise an `AssertionError` if the issue is present.