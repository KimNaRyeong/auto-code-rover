Here is the reproducer script:

```python
import django
from django.db import models

def main():
    try:
        class Document(models.Model):
            pass

        class Picking(Document):
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

        models.get_model('Document')
    except django.core.exceptions.ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError("Expected ImproperlyConfigured exception")

    if __name__ == "__main__":
        main()
```

This script defines the same model structure as described in the issue, and then attempts to get the models. If an `ImproperlyConfigured` exception is raised, it prints the stack trace using the provided function and raises an `AssertionError`.