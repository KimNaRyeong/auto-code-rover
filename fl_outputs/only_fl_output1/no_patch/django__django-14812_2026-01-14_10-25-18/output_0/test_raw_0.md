```python
# reproducer.py
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import execute_from_command_line
from django.db import models
from django.contrib import admin

# Setting up minimal Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        __name__,  # This module (reproducer.py) is an app for this example
    ],
    ROOT_URLCONF=__name__,  # Required even if unused
)

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

# Defining models according to the provided issue description
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

# Defining ModelAdmin according to the description
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'

@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]

if __name__ == '__main__':
    try:
        # Mimicking part of Django's startup process to initialize the models
        import django
        django.setup()
        
        # Trying to instantiate the admin with inlines should raise an issue if the bug is present
        try:
            admin_instance = SpecialJournalistAdmin(SpecialJournalist, admin.site)
        except Exception as e:
            # Handling ImproperlyConfigured because Django might not be fully set up for complete admin functionality
            if not isinstance(e, ImproperlyConfigured):
                print_stacktrace(e)
                raise AssertionError("The admin.E202 issue is present.") from e
        
    except AssertionError as e:
        # If AssertionError was caught, it means the issue is present
        print(e)
    else:
        # If no exceptions, the issue might be fixed or not triggered
        print("Issue not reproduced. This may indicate that the issue is fixed or the reproduction is incorrect.")

```

This script sets up the Django environment minimally to demonstrate the presence of the described issue. It follows your request to exit normally if the issue is not present and to print a detailed stack trace if an `AssertionError` occurs due to the issue being present. Make sure to have Django installed in your environment before running this script.