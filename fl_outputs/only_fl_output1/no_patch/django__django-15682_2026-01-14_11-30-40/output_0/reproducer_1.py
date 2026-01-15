# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models

# configure settings for the Django project
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(os.getcwd(), "db.sqlite3"),
        }
    },
    INSTALLED_APPS=['__main__'],  # This script is the app
    USE_TZ=True,
)

django.setup()

# Define the model
class TemplateVersion(models.Model):
    published_at = models.DateTimeField(null=True)

    class Meta:
        app_label = '__main__'


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

def main():
    # Create necessary tables
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(TemplateVersion)
    
    # Insert test data into the TemplateVersion model
    TemplateVersion.objects.bulk_create([
        TemplateVersion(published_at=None),
        TemplateVersion(published_at='2022-02-25 13:00:12.091916+00:00'),
        TemplateVersion(published_at='2022-02-21 10:18:00.169248+00:00')
    ])

    # Attempt to reproduce the issue
    try:
        base_order_query = TemplateVersion.objects.order_by
        nulls_first_false = list(base_order_query(models.F("published_at").desc(nulls_first=False)))
        nulls_first_true = list(base_order_query(models.F("published_at").desc(nulls_first=True)))

        nulls_last_false = list(base_order_query(models.F("published_at").desc(nulls_last=False)))
        nulls_last_true = list(base_order_query(models.F("published_at").desc(nulls_last=True)))

        assert nulls_first_false != nulls_first_true, "Expected different results for nulls_first False and True"
        assert nulls_last_false != nulls_last_true, "Expected different results for nulls_last False and True"
        
        print("The test Passed! The behaviours are consistent and valid.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
