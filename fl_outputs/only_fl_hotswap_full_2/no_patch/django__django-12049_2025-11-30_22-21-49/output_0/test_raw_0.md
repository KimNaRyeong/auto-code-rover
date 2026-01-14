 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.management import execute_from_command_line
from django.db import connections, DEFAULT_DB_ALIAS
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
    settings = {
        'DATABASES': {
            DEFAULT_DB_ALIAS: {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'my_DB',
                'USER': 'my_user',
                'PASSWORD': 'my_password',
                'HOST': 'localhost',
                'PORT': '3306',
                'OPTIONS': {
                    'init_command': "SET collation_connection = 'utf8_general_ci'; SET NAMES 'utf8';",
                    'charset': 'utf8mb4',
                    'autocommit': True,
                    'lower_case_table_names': 0,
                }
            }
        },
        'INSTALLED_APPS': [
            'my_first_app',
        ],
    }

    sys.path.append('.')
    sys.path.append('..')
    from django.conf import __file__ as conf_file
    with open(conf_file) as f:
        exec(f.read(), settings)

    execute_from_command_line(['django', 'migrate', '--database', DEFAULT_DB_ALIAS, '--fake-initial', 'my_first_app'])

if __name__ == '__main__':
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, create a new Django project with the following structure:
```diff
- my_project/
  - my_first_app/
    - migrations/
      - __init__.py
      - 0001_initial.py
    - models.py
    - tests.py
  - manage.py
  - reproducer.py
```
In `my_project/settings.py`, add the following code:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_DB',
        'USER': 'my_user',
        'PASSWORD': 'my_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET collation_connection = 'utf8_general_ci'; SET NAMES 'utf8';",
            'charset': 'utf8mb4',
            'autocommit': True,
            'lower_case_table_names': 0,
        }
    }
}

INSTALLED_APPS = [
    'my_first_app',
]
```
In `my_project/my_first_app/models.py`, add the following code:
```python
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    countrycode = models.ForeignKey('Country', on_delete=models.CASCADE, db_column='countryCode')

class Country(models.Model):
    name = models.CharField(max_length=100)
```
In `my_project/my_first_app/migrations/0001