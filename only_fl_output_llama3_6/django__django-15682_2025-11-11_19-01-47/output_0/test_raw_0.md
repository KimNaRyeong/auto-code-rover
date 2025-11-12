Here is the reproducer script:

```python
import django
from django.db.models import F, DateTimeField
from django.db import models

def main():
    class TemplateVersion(models.Model):
        published_at = models.DateTimeField(null=True)

    try:
        template_versions = TemplateVersion.objects.all()
        nulls_first_result = list(template_versions.order_by(F("published_at").desc(nulls_first=False)))
        nulls_last_result = list(template_versions.order_by(F("published_at").desc(nulls_last=False)))

        if nulls_first_result != [None, datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>), datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>)]:
            raise AssertionError("Expected nulls_first_result: {}".format(nulls_first_result))
        if nulls_last_result != [None, datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>), datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>)]:
            raise AssertionError("Expected nulls_last_result: {}".format(nulls_last_result))
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a simple Django model with a DateTimeField that can be null. It then uses the F expression to order the objects by the published_at field in descending order, first with `nulls_first=False` and then with `nulls_last=False`. If the results are not as expected (i.e., the null values are at the beginning), it raises an AssertionError and prints a stack trace.