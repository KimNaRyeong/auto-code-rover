Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.core.management import execute_from_command_line

def main():
    # Create a new Django project
    os.makedirs('myproject', exist_ok=True)
    os.chdir('myproject')
    with open('settings.py', 'w') as f:
        f.write('''
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
''')

    execute_from_command_line(['manage.py', 'startapp', 'mymodel'])

    # Create the model
    with open('mymodel/models.py', 'w') as f:
        f.write('''
from django.db import models

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)
''')

    # Run the migrations
    execute_from_command_line(['manage.py', 'migrate'])

    try:
        from mymodel.models import MyModel
        obj = MyModel.objects.create(value=float('nan'))
        obj.refresh_from_db()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not present")

    # Run the admin view to reproduce the issue in the changelist view
    execute_from_command_line(['manage.py', 'runserver'])
    import time
    time.sleep(1)  # Wait for the server to start
    os.system('curl http://localhost:8000/admin/mymodel/mymodel/1/change/')

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

if __name__ == '__main__':
    main()
```

This script creates a new Django project, defines the `MyModel` model with a `DecimalField`, runs the migrations, and then attempts to create an instance of the model with a NaN value. It also tries to refresh the object from the database, which should raise a `TypeError`.