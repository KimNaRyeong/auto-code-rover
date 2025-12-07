 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import sys
import django
from django.db import migrations, models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_test():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    django.setup()

    # Create a new Django project
    project_name = "test_project"
    django.dispatch.Signal.send(sender=django.__name__, signal=django.core.signals.setup_project,
                                project=project_name)

    # Create a new app called myapp
    app_name = "myapp"
    django.dispatch.Signal.send(sender=django.__name__, signal=django.core.signals.setup_app, app=app_name)

    # Define a model for the app
    class MyModel(models.Model):
        name = models.CharField(max_length=100)
        age = models.IntegerField()

        class Meta:
            constraints = [
                migrations.CheckConstraint(
                    check=models.Q(age__gte=1),
                    name="Age should not be.less.than.one."
                )
            ]

    # Create the initial migration for the app
    migrations.makemigrations(app_name)

    # Apply the initial migration for the app
    migrations.migrate(app_name)

    # Check if the migration was applied
    applied_migrations = migrations.show_migrations()
    if f"0001_initial" not in applied_migrations[app_name]:
        raise AssertionError("Initial migration not applied")

    # Check if the new migration was created
    new_migration_name = f"0002_{app_name}_age should not be.less.than.one."
    if new_migration_name not in os.listdir(os.path.join(os.path.dirname(__file__), app_name, "migrations")):
        raise AssertionError(f"New migration '{new_migration_name}' not created")

    # Apply the new migration
    migrations.migrate(app_name)

    # Check if the new migration was applied
    applied_migrations = migrations.show_migrations()
    if new_migration_name not in applied_migrations[app_name]:
        raise AssertionError(f"New migration '{new_migration_name}' not applied")

if __name__ == "__main__":
    try:
        run_test()
        print("Test passed")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script creates a new Django project and app, defines a model with a constraint that requires a migration, and applies the migrations. If the new migration is not detected by Django, the script raises an `AssertionError` with a stack trace.

To run the script, create a new Django project with the following directory structure:
```markdown
test_project/
├── manage.py
├── test_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── myapp/
    ├── __init__.py
    ├── migrations/
    │   └── __init__.py
    └── models.py
```
Then, run the script with `python3 reproducer.py`. If the issue is present, the script will raise an `AssertionError` and