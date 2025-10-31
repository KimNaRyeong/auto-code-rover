Here is the reproducer script:

```python
import unicodedata
from django.utils.text import slugify
from django.db.models import Model
from django.db.models.fields.related_descriptors import RelatedDescriptor

class Page(Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

def main():
    page = Page(title="Hello İstanbul")
    try:
        page.slug = slugify(page.title, allow_unicode=True)
        page.full_clean()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected ValidationError")

if __name__ == "__main__":
    main()
```

This script creates a `Page` object with the title "Hello İstanbul", attempts to set its slug using `slugify`, and then calls `full_clean`. If an exception is raised, it prints the stack trace and raises an `AssertionError`.