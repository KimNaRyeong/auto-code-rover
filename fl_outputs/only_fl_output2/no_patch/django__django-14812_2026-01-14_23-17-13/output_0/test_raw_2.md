To create a standalone Python file `reproducer.py` that reproduces the outlined issue in a Django project, follow these steps:

1. Ensure Django is installed in your environment.
2. Use the following code snippet, which serves as the content of `reproducer.py`, positioned at the root directory of your Django project.
3. Execute this script using `python3 reproducer.py`.

This script sets up models according to your description and attempts to register an admin class that would trigger the `AssertionError` if the issue with proxy models and ForeignKey references is present, otherwise, it exits with code 0 indicating no issue was found. It includes your requested function to print stack traces clearly.

```python
"""
reproducer.py
"""
import os
import sys
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.core.management import execute_from_command_line


# Definition of the models according to the specifications
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


# Definition of the inline admin according to the specifications
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'


# Definition of the model admin according to the specifications
@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


# Function to print stack traces clearly
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


# Setup Django environment programmatically
def setup():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='a-very-secret-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            '__main__',  # This script is its own Django app
        ],
        USE_I18N=True,
        USE_L10N=True,
    )

    try:
        execute_from_command_line(['manage.py', 'migrate'])
    except SystemExit as e:  # Handle the system exit that `migrate` might cause.
        pass
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)


if __name__ == '__main__':
    setup()

    # Test if the issue is present or not
    try:
        admin.site.check()
        # Assume issue is fixed if no errors
        print("The issue seems to be fixed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

Here are important notes regarding this script:
- This script configures a Django environment dynamically and includes model and admin site registration inline, making it a self-contained example for reproducing the issue.
- It then runs migrations to ensure the setup is capable of simulating the application's real-world usage.
- Run this script in an environment where Django is already installed. If not installed, you can install Django using pip: `pip install django`.
- The existence of an `AssertionError` indicates the problem simulates correctly; the script exits with code 1. If the stack trace shows a different exception, it may highlight an issue with the script or environment setup rather than reproducing the specified admin issue.