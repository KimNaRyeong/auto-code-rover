Here is the reproducer script:

```python
import os
from django.db import migrations
from django.test.utils import setup_test_environment
from django.test.runner import DiscoverRunner
from django.core.management import execute_from_command_line
from django.conf import settings

def main():
    # Set up Django environment for testing
    settings.configure({
        'DATABASES': {
            'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test_default.db'},
            'non_default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test_non_default.db'}
        }
    })
    setup_test_environment()
    
    # Create a test database with the router
    from project.routers import Router
    
    class TestRouter(Router):
        def allow_migrate(self, db, model):
            if db == 'default':
                return True
            return False

    from django.test.utils import setup_databases
    setup_databases(test_db_name='test_default', databases={'default': 'sqlite:///test_default.db', 'non_default': 'sqlite:///test_non_default.db'})
    
    # Run the migrate command to reproduce the issue
    try:
        execute_from_command_line(['manage.py', 'migrate', '--database', 'non_default'])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script sets up a Django environment for testing, creates a test database with the router, runs some tests to ensure that everything is set up correctly, and then attempts to run the migrate command on a non-default database. If any exceptions occur during this process, it prints the stack trace and raises an AssertionError.

Please note that you need to replace `'project'` with your actual Django project name.