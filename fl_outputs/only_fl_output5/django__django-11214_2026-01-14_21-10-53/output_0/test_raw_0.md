```python
# reproducer.py
import os
import sys
from django.core.management import call_command
from django.db import migrations, models
from django.db.migrations.recorder import MigrationRecorder

# Updating the environment variable for Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

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

def assert_migration_issue():
    try:
        # Simulating creating an initial migration with a CheckConstraint containing a range
        migration = migrations.Migration(
            "test_migration", "app_name"
        )
        migration.operations = [
            migrations.AddConstraint(
                model_name='monthlybudget',
                constraint=models.CheckConstraint(
                    check=models.Q(month__in=range(1, 13)),
                    name='check_valid_month'
                ),
            )
        ]
        
        # Applying the migration to simulate the environment
        recorder = MigrationRecorder.Migration.objects.create(
            app="app_name",
            name="test_migration"
        )
        
        # Running makemigrations to detect changes
        call_command("makemigrations", "app_name", check=True)
        
        # Trying to retrieve the newly created migration file
        latest_migration = MigrationRecorder.Migration.objects.filter(
            app="app_name"
        ).latest("applied")

        if latest_migration.name != recorder.name:
            raise AssertionError("New migration was created due to constraint check inconsistency.")
        
        print("Issue not found. No unexpected migrations generated.")
        sys.exit(0)
    
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to verify the migration issue.") from e

if __name__ == "__main__":
    assert_migration_issue()
```

**Note:** To use this script, you need to replace `"your_project.settings"` with the actual Django settings module path of your project. Also, replace `"app_name"` with the actual Django app name where you're testing this constraint issue. This script assumes the Django environment is properly set up and the `monthlybudget` model already exists in your app. Furthermore, for a true standalone test, additional setup may be required, like dynamically creating the model or setting up the Django project within the script, which is beyond this script's current scope.