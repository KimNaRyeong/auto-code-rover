Here is the revised standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys

from django.conf import settings
from django.db import models
from django.contrib import admin

# Set up Django environment
settings.configure(
    INSTALLED_APPS=['django.contrib.admin', 'django.contrib.contenttypes'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
)

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Define models
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

# Define admin
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'

@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]

try:
    # Try to access the admin interface
    admin.autodiscover()
    admin.site._setup()
    SpecialJournalistAdmin(SpecialJournalist, admin.site).inlines[0].formset
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue is present"
else:
    print("Issue is fixed")
    sys.exit(0)
```
This script sets up a Django environment with the models and admins defined in the issue description. It then tries to access the admin interface, which should raise an `AssertionError` if the issue is present. If no exception is raised, it prints "Issue is fixed" and exits with code 0.

Please run this script by executing `python3 reproducer.py` in the root directory of your project.