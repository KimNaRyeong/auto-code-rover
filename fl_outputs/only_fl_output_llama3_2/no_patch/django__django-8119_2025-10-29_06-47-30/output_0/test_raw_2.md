Here is the reproducer script:

```python
from django.db import models
from django.db.models.functions import Lower

def main():
    try:
        MyModel.objects.filter(F('some_field').lower() == 'anssi')  # This line should raise an exception
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception")

if __name__ == "__main__":
    main()
```

This script attempts to use the `F` expression in a filter call, which should raise an exception if the issue is present.