import os
import django
from django.conf import settings
from django.db import models, connection
from django.db.models import F

# Inline Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # Add this script as an app
    ),
    USE_TZ=True,
)

django.setup()

# Define the model after setting up Django.
class TemplateVersion(models.Model):
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = '__main__'


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

def run_test():
    # Create the table for TemplateVersion
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TemplateVersion)

    # Setup - create instances
    TemplateVersion.objects.create(published_at=None)
    TemplateVersion.objects.create(published_at="2022-02-25T13:00:12.091916Z")
    TemplateVersion.objects.create(published_at="2022-02-21T10:18:00.169248Z")

    # Test the behavior
    try:
        result_nulls_first_false = [tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=False))]
        result_nulls_last_false = [tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=False))]

        # The issue description implies that both queries should produce different orderings, but they don't due to the bug.
        # Hence, if they produce the same result, the issue is present.
        assert result_nulls_first_false != result_nulls_last_false, "Expected different orderings for nulls_first=False and nulls_last=False."

    except AssertionError as e:
        print_stacktrace(e)
        raise

    print("Issue not present. Test passed.")

if __name__ == "__main__":
    run_test()
