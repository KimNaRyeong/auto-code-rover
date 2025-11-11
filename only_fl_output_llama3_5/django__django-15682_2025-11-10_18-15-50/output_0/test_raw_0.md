Here is the reproducer script:

```python
import django
from django.db.models import F, DateTimeField
from django.db import models

def main():
    class TemplateVersion(models.Model):
        published_at = models.DateTimeField(null=True)

    try:
        template_versions = TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=False))
        if [tv.published_at for tv in template_versions] != [
            None,
            datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
            datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>)
        ]:
            raise AssertionError("Expected ordering")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a simple Django model with a DateTimeField that can be null. It then orders the objects by this field in descending order, first considering nulls to come first (nulls_first=True). The expected result is that all null values are at the beginning of the list, followed by the non-null values in descending order.

If the actual result does not match the expected result, an AssertionError is raised and the stack trace is printed.