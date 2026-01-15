To create a standalone script `reproducer.py` that automates the reproduction of the described Django migration issue, we'll need to perform the following steps in the script:

1. Simulate the creation of a Django project and app.
2. Generate initial migrations and apply them.
3. Add a model constraint that introduces the naming issue in the migration file.
4. Attempt to create and apply the problematic migration.

The script will use Django's management commands programmatically and will assess the presence of the issue based on whether the expected migration file is created and detected correctly. On encountering the issue, it'll raise an `AssertionError`.

Here's how the `reproducer.py` script could look:

```python
import os
import sys
import subprocess
from django.core import management
from django.conf import settings

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

# Configuration to run Django without a full project setup
def configure_django():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=(
            'myapp',
        ),
        BASE_DIR=os.path.dirname(os.path.abspath(__file__)),
    )

def create_app():
    try:
        os.mkdir('myapp')
        with open('myapp/__init__.py', 'w'):
            pass
        with open('myapp/models.py', 'w') as f:
            f.write("""
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
""")
        with open('myapp/apps.py', 'w') as f:
            f.write("""
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'myapp'
""")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def generate_migrations():
    management.call_command('makemigrations', 'myapp')

def apply_migrations():
    management.call_command('migrate')

def add_constraint_and_migrate():
    with open('myapp/models.py', 'w') as f:
        f.write("""
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
""")
    management.call_command('makemigrations', 'myapp')
    migration_files = os.listdir(os.path.join('myapp', 'migrations'))
    assert '0002_mymodel_age_should_not_be_less_than_one.py' in migration_files, "Expected migration not generated."

if __name__ == "__main__":
    try:
        configure_django()
        create_app()
        generate_migrations()
        apply_migrations()
        add_constraint_and_migrate()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as general_exception:
        print_stacktrace(general_exception)
        sys.exit(1)

    print("Migration file naming issue fixed.")
    sys.exit(0)
```

**Note:** This script assumes you have Django installed in your environment and the script is executed in a suitable environment where Django commands can be invoked. If run outside such an environment, it may fail due to missing dependencies or configurations. Ensure Django is installed (`pip install Django`) and adjust the script to fit into the actual structure of your Django project if necessary.