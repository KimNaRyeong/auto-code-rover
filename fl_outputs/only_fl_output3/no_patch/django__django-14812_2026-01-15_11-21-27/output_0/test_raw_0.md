```python
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib import admin
import os
import sys

# Configure Django settings
settings.configure(
    INSTALLED_APPS=(
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

# Initialize Django
import django
django.setup()


# Models definition
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


# Admin definition
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'

try:
    @admin.register(SpecialJournalist)
    class SpecialJournalistAdmin(admin.ModelAdmin):
        inlines = [ArticleInline]

    # Test to trigger the checks
    from django.contrib.admin.sites import AdminSite
    site = AdminSite()
    site.register(SpecialJournalist, SpecialJournalistAdmin)

    # Verification of the assertion
    # If this line is reached without an exception, the issue is fixed.
    print("Issue is fixed.")
except Exception as e:
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

    print_stacktrace(e)
    assert isinstance(e, ImproperlyConfigured), "An unexpected error type was raised."

```
This script sets up a minimal Django environment, defines the models, and registers them with the Django admin, following the scenario described in the issue. If the issue is present, it tries to reproduce the check that's failing (the admin registration and inline model registration throw an exception regarding the ForeignKey reference). Specifically, it captures the exception, prints the stack trace as requested, and asserts the type of exception to ensure it's the expected one being thrown due to the issue. If the issue is fixed, the script simply prints a message indicating success.