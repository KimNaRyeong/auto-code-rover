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
        assert not any(tv.published_at is None for tv in template_versions)
    except AssertionError as e:
        print_stacktrace(e)
        raise

    try:
        template_versions = TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=False))
        assert not any(tv.published_at is None for tv in template_versions)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a simple Django model and then attempts to order the objects by their `published_at` field with `nulls_first=False` and `nulls_last=False`. If either of these assertions fail, it prints the stack trace and raises an `AssertionError`.