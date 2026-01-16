import os
import django
from django.conf import settings
from django.core.management import call_command

# Configure settings for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase.db',
        }
    },
    INSTALLED_APPS=['__main__'],
    SECRET_KEY='a-very-secret-key',
    USE_I18N=False,
    USE_L10N=False,
    USE_TZ=False,
)

# Initialize Django
django.setup()

from django.db import models

# Define the Article model
class Article(models.Model):
    slug = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="unique_slug")
        ]

# Create the tables
call_command('migrate', '--noinput')

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

def test_in_bulk_with_unique_constraint():
    try:
        # Attempt to invoke in_bulk() with field_name="slug"
        result = Article.objects.in_bulk(field_name="slug")
        print(f"Result: {result}")
    except ValueError as e:
        assert "in_bulk()'s field_name must be a unique field but" in str(e), "Unexpected ValueError message."
        print_stacktrace(e)
        raise AssertionError("Issue is present") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected exception occurred") from e
    else:
        print("No ValueError, issue may be resolved.")

if __name__ == '__main__':
    test_in_bulk_with_unique_constraint()
