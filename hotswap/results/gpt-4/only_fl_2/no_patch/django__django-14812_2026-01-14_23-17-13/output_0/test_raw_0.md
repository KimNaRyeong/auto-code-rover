Below is a standalone Python script named `reproducer.py`. This script sets up a minimal Django project to reproduce the described issue. To run it, ensure Django is installed in your environment (you can install it using `pip install Django`). 

```python
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.contrib import admin

# Configure Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    INSTALLED_APPS=(
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',  # This script
    ),
    ROOT_URLCONF='__main__',
)


# Define models according to the issue description
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


# Define the Admin inline
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'


# Define the SpecialJournalistAdmin
@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


# Function to print the stack trace as per the requirement
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


def run_checks():
    try:
        # Execute Django checks to trigger the issue
        execute_from_command_line(['manage.py', 'check'])

    except Exception as e:
        # If there's an error, print the stack trace and re-raise
        print_stacktrace(e)
        raise


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
    try:
        admin.autodiscover()  # Attempt to register admin models and check for errors
        run_checks()  # Specifically check for any issues
        print("No issues detected. If you're seeing this message, it means the issue has been fixed.")
    except AssertionError as e:
        print("Assertion Error: The issue is present.")
        print_stacktrace(e)
        sys.exit(1)
```

This script setups a minimal Django environment with models and admin definitions that simulate the issue as described. It tries to execute Django checks, and if any exceptions related to the issue are caught, it prints the stack trace using the provided function. If the issue is fixed, or no exception is related to this issue, it will print a message saying no issues were detected.