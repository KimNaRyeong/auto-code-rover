 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.management import execute_from_command_line
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    executable = sys.executable
    args = [executable, "-m", "django", "migrate", "--database", "my_DB", "--fake-initial", "my_first_app"]
    try:
        execute_from_command_line(args)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Applied migration detection may fail when using a case-insensitive collation"

if __name__ == "__main__":
    # Create a dummy Django project and app
    executable = sys.executable
    args = [executable, "-m", "django", "startproject", "my_project"]
    execute_from_command_line(args)

    with open("my_project/settings.py", "a") as f:
        f.write("\nDATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.mysql',\n        'NAME': 'my_DB',\n        'USER': 'root',\n        'PASSWORD': '',\n        'HOST': 'localhost',\n        'PORT': '3306',\n        'OPTIONS': {\n            'init_command': 'SET collation_connection = utf8_general_ci; SET NAMES utf8;',\n            'charset': 'utf8mb4',\n        }\n    }\n}\n")

    args = [executable, "-m", "django", "startapp", "my_first_app"]
    execute_from_command_line(args)

    # Create a dummy model with a field that has a different case than the table column
    with open("my_first_app/models.py", "w") as f:
        f.write("from django.db import models\n\nclass City(models.Model):\n    countrycode = models.ForeignKey(db_column='countryCode', on_delete=models.CASCADE, to='my_DB.Country')")

    # Create a migration file
    args = [executable, "-m", "my_first_app", "makemigrations"]
    execute_from_command_line(args)

    # Reproduce the issue
    reproduce_issue()
```
To reproduce the issue, create a new Django project and app, create a dummy model with a field that has a different case than the table column, create a migration file, and then run the `reproduce_issue()` function. The function runs the `python3 manage.py migrate --database my_DB --fake-initial my_first_app` command, which should fail with an `OperationalError` due to the case-insensitive collation.

The `print_stacktrace()` function is used to print a stack trace of the issue. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.