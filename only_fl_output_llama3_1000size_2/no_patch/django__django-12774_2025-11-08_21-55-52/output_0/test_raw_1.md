Here is the reproducer script:

```python
import os
from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings

def main():
    if not settings.configured:
        settings.configure()

    class Article(models.Model):
        slug = models.CharField(max_length=255)

        class Meta:
            constraints = [
                UniqueConstraint(fields=["slug"], name="%(app_label)s_%(class)s_slug_unq")
            ]

    try:
        articles = Article.objects.in_bulk(field_name="slug")
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before defining the model. This should allow the model to be defined and the issue to be reproduced.