```python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

# Configure Django. This minimal setup is enough to reproduce the issue.
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.admin",
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    }
)

# Initialize Django
execute_from_command_line(['manage.py', 'migrate'])


from django.db import models
from django.contrib import admin

# Define models and admin classes to reproduce the issue.
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

class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'

@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


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

# Attempt to reproduce the issue.
try:
    admin.site.check()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("The issue is present.") from e
else:
    print("The issue is fixed.")

```

This script initializes a Django project, defines the required models to reproduce the issue, and then uses Django's system checks to confirm if the problem exists (i.e., if `admin.E202` is raised because `fk_name 'journalist' is not a ForeignKey to 'SpecialJournalist'`). It prints a detailed stack trace if an exception occurs and raises an `AssertionError` to signal the presence of the issue.