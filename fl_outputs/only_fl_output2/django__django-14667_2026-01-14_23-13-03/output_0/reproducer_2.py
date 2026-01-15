import os
import django
from django.conf import settings
from django.db import models
from django.apps import apps

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=["__main__"],
    USE_TZ=True,
)
django.setup()

# Define the Company model
class Company(models.Model):
    name = models.CharField(max_length=100)
    trade_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

# Run migrations
apps.populate(settings.INSTALLED_APPS)
django.core.management.call_command("migrate", "--noinput")

# Function to print stack trace
def print_stacktrace(e: Exception):
    import traceback
    import sys

    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    line {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Main function to execute queries
def main():
    # Execute the queries that might demonstrate the issue
    try:
        # Interrogate the SQL of the problematic query
        query_1 = str(Company.objects.only("name").defer("name").query)
        query_2 = str(Company.objects.only("name").defer("name").defer("country").query)

        # Assertions to verify the unexpected behavior
        assert "trade_number" not in query_1, "Query unexpectedly contains 'trade_number'."
        assert "country" not in query_1, "Query unexpectedly contains 'country'."
        assert "trade_number" not in query_2, "Query unexpectedly contains 'trade_number'."
        assert "country" not in query_2, "Query unexpectedly contains 'country'."

        # If assertions pass, we expect the issue is not present
        print("Issue not present or assertions did not fail as expected.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Ensure to exit with a non-zero status code if assertion fails

if __name__ == "__main__":
    main()
