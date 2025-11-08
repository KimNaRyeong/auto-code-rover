I apologize for the previous mistake. Here is a new reproducable script:

```python
import django
from django.db import models

def main():
    try:
        class Document(models.Model):
            pass

        class Picking(Document):
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')

        models.get_model('Document')
    except django.core.exceptions.ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError("Expected ImproperlyConfigured exception")

    if __name__ == "__main__":
        main()
```

This script defines the same model structure as described in the issue, but with the order of OneToOneField swapped. This should reproduce the issue and raise an `AssertionError` when run.