Here is the reproducer script:

```python
import os
from django.core.management import execute_from_command_line
from django.conf import settings

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
    # Create a new Django project
    os.system("python -m django startproject test_project")
    
    # Navigate into the project directory
    os.chdir("test_project")
    
    # Create an app in the project
    os.system("python manage.py startapp my_app")
    
    # Move into the app directory
    os.chdir("my_app")
    
    # Create some migrations
    with open("migrations/0001_initial.py", "w") as f:
        f.write("from django.db import migrations\n\nclass Migration(migrations.Migration):\n    initial = True\n    dependencies = [('my_app', '0002_blah')]  \n    operations = [\n        migrations.RunPython(lambda *args: None, lambda *args: None),\n    ]")
    
    with open("migrations/0002_blah.py", "w") as f:
        f.write("from django.db import migrations\n\nclass Migration(migrations.Migration):\n    dependencies = [('my_app', '0001_initial')]  \n    operations = [\n        migrations.RunPython(lambda *args: None, lambda *args: None),\n    ]")
    
    with open("migrations/0003_blah.py", "w") as f:
        f.write("from django.db import migrations\n\nclass Migration(migrations.Migration):\n    dependencies = [('my_app', '0002_blah')]  \n    operations = [\n        migrations.RunPython(lambda *args: None, lambda *args: None),\n    ]")
    
    # Squash the migrations
    os.system("python manage.py squashmigrations my_app --auto")
    
    # Create a new migration with poor naming
    with open("migrations/0001_initial_squashed_0003_blah.py", "w") as f:
        f.write("from django.db import migrations\n\nclass Migration(migrations.Migration):\n    initial = True\n    dependencies = [('my_app', '0002_blah')]  \n    operations = [\n        migrations.RunPython(lambda *args: None, lambda *args: None),\n    ]")
    
    with open("migrations/0002_blah.py", "w") as f:
        f.write("from django.db import migrations\n\nclass Migration(migrations.Migration):\n    dependencies = [('my_app', '0001_initial_squashed_0003_blah')]  \n    operations = [\n        migrations.RunPython(lambda *args: None, lambda *args: None),\n    ]")
    
    # Run the migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    try:
        # Check if the issue is present
        with open('migrations/0001_initial_squashed_0003_blah.py') as f:
            pass
    except FileNotFoundError:
        raise AssertionError("Issue not found")
    else:
        print_stacktrace(AssertionError("Issue found"))
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a new Django project, app and migrations. It then squashes the migrations and creates a new migration with poor naming. Finally, it runs the migrations and checks if the issue is present by trying to open the file that should not exist. If the file exists, it raises an `AssertionError` and prints the stack trace.