Here is the standalone Python file `reproducer.py` that reproduces the issue:
```python
import django
from django.contrib import admin
from django.db import models

# Define the models
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

# Define the model admins
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'

@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]

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
    admin.site.register(SpecialJournalist, SpecialJournalistAdmin)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```
This script defines the same models and model admins as described in the issue description. It then attempts to register the `SpecialJournalist` model with its custom admin class using `admin.site.register()`. If an `AssertionError` is raised, it prints the stack trace using the provided function and exits with code 1.

To run this script, save it to a file named `reproducer.py` in the root directory of your project and execute it using `python3 reproducer.py`. This should reproduce the issue and print the stack trace.