Here is the reproducer script:

```python
import os
from django.db import IntegrityError
from django.core.management import execute_from_command_line
from django.conf import settings
from django.test.utils import setup_test_environment
from django.core.exceptions import AssertionError

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    settings.configure()
    setup_test_environment()
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    
    from django.db import connection
    from project.models import Foo, Bar
    
    # Create models
    class Bar(models.Model):
        pass
    class Foo(models.Model):
        bar = models.ManyToManyField('Bar', blank=True)
        
    # Migrate
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Change type of the ManyToManyField to Foo
    class Bar(models.Model):
        pass
    class Foo(models.Model):
        bar = models.ManyToManyField('Foo', blank=True)
        
    # Migrate (see above)
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    try:
        # In the admin page, navigate to "add Foo", click save
        foo = Foo()
        foo.save()
    except IntegrityError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")
    else:
        print("Issue not present")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script should be placed in the root directory of your Django project.