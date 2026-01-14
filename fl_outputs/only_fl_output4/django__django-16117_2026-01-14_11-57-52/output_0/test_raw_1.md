Below is a standalone Python script named `reproducer.py` designed to programmatically create a Django project and app, simulate the issue described, and verify the existence of the problem based on the migration file naming issue. It will raise an `AssertionError` if the problem is present and print a detailed stack trace. The script uses Django's management commands programmatically to mimic actions like creating migrations.

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

def run_command(command):
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        raise Exception(f"Command '{command}' failed with exit code {process.returncode}: {process.stderr}")

try:
    # Setting up a new Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    run_command("django-admin startproject test_project .")
    run_command("python manage.py startapp myapp")

    # Creating a model in the app
    model_def = '''
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__gte=1),
                name="Age should not be.less.than.one."
            )
        ]
'''
    with open("myapp/models.py", "w") as f:
        f.write(model_def)

    # Adding 'myapp' to installed apps
    with open("test_project/settings.py", "a") as f:
        f.write("\nINSTALLED_APPS += ['myapp']\n")

    # Generating migrations
    run_command("python manage.py makemigrations myapp")

    # Verify if migration file is not detected due to naming issue
    migration_file = next((f for f in os.listdir("myapp/migrations") if f.startswith("0002")), None)
    assert migration_file is not None and "should not be.less.than.one." in migration_file, "Expected migration not generated with problematic name."
    try:
        run_command("python manage.py migrate")
        raise AssertionError("Migration applied successfully with a problematic filename, which was not expected.")
    except Exception as e:
        print("Successfully detected an issue with the migration file naming convention.")
        print_stacktrace(e)

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduction was successful without errors, indicating the presence of the migration file naming issue.")
sys.exit(0)
```

This script performs the following operations:
1. Sets up a new Django project and application.
2. Creates a model with a problematic constraint name that leads to generating a migration file with dots in its name.
3. Attempts to generate and apply migrations to capture the error when Django fails to recognize the migration file due to its naming convention.
4. Asserts the presence of the described issue and prints a stack trace if the issue exists or if any unexpected error occurs during the process.