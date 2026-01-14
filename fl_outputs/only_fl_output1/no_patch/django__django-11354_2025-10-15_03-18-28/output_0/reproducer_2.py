import os
import sys
import django
from django.conf import settings
from django.db import models, migrations, connection
from django.db.models.expressions import RawSQL

# Function to print stack trace
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

# Dynamically configure the Django settings with the minimum necessary to run the app
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test_db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This tells Django to load the app's models below
    ],
    USE_TZ=True,
)

django.setup()

# Define models after setup to ensure Django is ready to work with them
class BaseItem(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        app_label = '__main__'

class Item(BaseItem):
    class Meta:
        app_label = '__main__'

# Entry point of the script
if __name__ == '__main__':
    # Create the tables
    with connection.schema_editor() as editor:
        editor.create_model(BaseItem)
        editor.create_model(Item)

    try:
        # Reproduce the issue
        queryset = Item.objects.annotate(title2=RawSQL("SELECT title AS title2 FROM __main__baseitem WHERE __main__baseitem.id = __main__item.id", ()))
        count = queryset.count()  # This line is expected to raise an error if the issue persists
        print(f"Counted {count} items without encountering the issue. The issue might have been resolved.")

    except Exception as e:
        print_stacktrace(e)
        assert False, "An exception was raised while attempting to count items. The issue likely persists."

    finally:
        # Optional: Clean up the database tables to avoid clutter
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(Item)
                editor.delete_model(BaseItem)
        except Exception as e:
            print("An error occurred during cleanup:", str(e))
