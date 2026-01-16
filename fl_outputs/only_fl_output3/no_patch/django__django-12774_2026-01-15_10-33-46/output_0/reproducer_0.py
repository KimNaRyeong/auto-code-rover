# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

# Minimal setup for Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=(
        "__main__",
    ),
    USE_I18N=True,
    USE_L10N=True,
)

django.setup()


class Article(models.Model):
    slug = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="%(app_label)s_%(class)s_slug_unq")
        ]


# Run setup
try:
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Article)
except Exception as e:
    pass  # In a real scenario, handle existing table or schema migration


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
        # Assumes that Articles have been created previously for this example
        result = Article.objects.in_bulk(field_name="slug")
        print("Test passed, no issues found.")
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("in_bulk() failed for field with UniqueConstraint.") from e


if __name__ == "__main__":
    test_in_bulk_with_unique_constraint()
