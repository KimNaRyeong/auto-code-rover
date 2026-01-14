To create a standalone script named `reproducer.py` that attempts to reproduce the described issue with Django migrations, you can follow the structure outlined below. This script programmatically creates a Django project and app, simulates the problematic behavior, and checks if the migration file with dots in its name fails to be recognized by Django's migration system.

For this script to function, ensure Django is installed in your environment. You can install Django using pip:

```bash
pip install django
```

Now, create the `reproducer.py` with the following content:

```python
import os
import subprocess
import sys

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

def check_migration_file_exists(file_path):
    return os.path.exists(file_path)

def setup_django_environment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    import django
    django.setup()

def main():
    test_project_dir = "temp_test_project"
    app_name = "myapp"
    migrations_dir = f"{test_project_dir}/{app_name}/migrations"

    # Clean up before start
    subprocess.run(f"rm -rf {test_project_dir}", shell=True)   
    
    try:
        # Step 1: Create a new Django project and app.
        subprocess.check_output(f"django-admin startproject test_project {test_project_dir}", shell=True)
        subprocess.check_output(f"cd {test_project_dir} && python manage.py startapp {app_name}", shell=True)
 
        # Step 2: Update settings.py to include new app.
        settings_path = os.path.join(test_project_dir, "test_project", "settings.py")
        with open(settings_path, "a") as settings_file:
            settings_file.write(f"\nINSTALLED_APPS += ['{app_name}',]\n")

        # Step 3: Create a model with constraints.
        models_path = os.path.join(test_project_dir, app_name, "models.py")
        with open(models_path, "w") as models_file:
            models_file.write("""
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__gte=1),
                name="Age.should.not.be.less.than.one."
            )
        ]
""")

        # Step 4: Make migrations
        subprocess.check_output(f"cd {test_project_dir} && python manage.py makemigrations {app_name}", shell=True)

        # Step 5: Check if migration file with dot in name is generated
        setup_django_environment()
        from django.db.migrations.loader import MigrationLoader
        loader = MigrationLoader(None, ignore_no_migrations=True)
        migration_names = loader.disk_migrations.keys()
        
        problematic_migration_name = any("age_should_not_be_less_than_one" in str(name) for app, name in migration_names)
        assert not problematic_migration_name, "Migration file with problematic name exists."

    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("The issue is fixed. Migration file naming issue is not present.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script works as follows:
1. Creates a new temporary Django project and an app named `myapp`.
2. Modifies the `settings.py` file to include the new app.
3. Overwrites the `models.py` file in the app to define a `MyModel` class with a constraint that should create a problematic migration file name.
4. Runs the `makemigrations` command for the app, which should generate the migration files.
5. Checks if a migration file with a name that's not conforming to the expected pattern exists by utilizing Django's internal `MigrationLoader`. If such a file is detected, it raises an `AssertionError`.
6. Cleans up by removing the temporary project directory.

Remember to run this script in an environment where Django is installed, and you have permissions to create and delete files and directories.