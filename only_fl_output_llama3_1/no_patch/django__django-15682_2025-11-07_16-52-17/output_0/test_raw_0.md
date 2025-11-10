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
        nulls_first_result = list(template_versions.order_by(F("published_at").desc(nulls_first=False)).values_list('published_at', flat=True))
        nulls_last_result = list(template_versions.order_by(F("published_at").desc(nulls_last=False)).values_list('published_at', flat=True))

        if nulls_first_result != [None, datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>), datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>)] or \
           nulls_last_result != [None, datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>), datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>)]:
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a simple Django model with a DateTimeField that can be null. It then orders the objects by this field in both ascending and descending order, using `nulls_first` and `nulls_last`. The results are checked to see if they match the expected output from the issue description. If they don't, an AssertionError is raised, which will print a stack trace when caught.