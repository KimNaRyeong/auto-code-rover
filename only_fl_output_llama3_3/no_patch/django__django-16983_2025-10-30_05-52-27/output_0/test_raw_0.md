Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple, FilteredVerticalTabularInline
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Article(models.Model):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, through='ArticleTag')

class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

def main():
    try:
        class MyAdmin(admin.ModelAdmin):
            filter_horizontal = ('tags',)
            inlines = [FilteredVerticalTabularInline]

        admin.site.register(Article, MyAdmin)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    django.setup()
    main()
```

This script creates a simple Django project with models and an admin interface. It then attempts to register the `Article` model in the admin interface with a custom admin class that uses `filter_horizontal` and `FilteredVerticalTabularInline`. If the issue is present, this should raise an `AssertionError` and print a stack trace.