Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib import admin
from django.contrib.admin import InlineModelAdmin, ModelAdmin

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    class Reporter(models.Model):
        name = models.CharField(max_length=50)

    class Journalist(Reporter):
        class Meta:
            proxy = True

    class SpecialJournalist(Journalist):
        class Meta:
            proxy = True

    class Article(models.Model):
        journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE)

    class ArticleInline(InlineModelAdmin):
        model = Article
        fk_name = 'journalist'

    class SpecialJournalistAdmin(ModelAdmin):
        inlines = [ArticleInline]

    admin.site.register(SpecialJournalist, SpecialJournalistAdmin)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

You can run this script by executing `python3 reproducer.py` in the root directory of your project. If the issue is present, it will raise an `AssertionError` and print a stack trace.