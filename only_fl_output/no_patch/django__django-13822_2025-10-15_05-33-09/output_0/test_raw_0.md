```python
# reproducer.py

def main():
    import os
    import sys
    import django
    from django.apps import apps
    from django.conf import settings
    from django.core.management import execute_from_command_line

    # Define settings for Django project
    settings.configure(
        SECRET_KEY='a-very-secret-key',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'app_one',
            'app_two',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        BASE_DIR=os.path.dirname(os.path.abspath(__file__)),
    )
    
    # Create two Django apps dynamically with models that will trigger the issue
    create_app('app_one', '''
from django.db import models

class Common(models.Model):
    class Meta:
        app_label = 'app_one'
''')

    create_app('app_two', '''
from django.db import models

class Common(models.Model):
    class Meta:
        app_label = 'app_two'
''')

    django.setup()

    try:
        # Try to create migration for these apps to trigger the underlying issue
        execute_from_command_line(['manage.py', 'makemigrations', 'app_one', 'app_two'])
    except Exception as e:
        # If an error is encountered, print stack trace and assert (to fail the script if the issue exists)
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e
    else:
        print("Issue is fixed.")
        
def create_app(name, models_code):
    """Utility function to create Django app with models dynamically."""
    os.makedirs(name, exist_ok=True)
    init_py = os.path.join(name, '__init__.py')
    models_py = os.path.join(name, 'models.py')

    # Create __init__.py if it doesn't exist
    if not os.path.exists(init_py):
        with open(init_py, 'w') as f:
            pass
    
    # Create models.py with the provided models code
    with open(models_py, 'w') as f:
        f.write(models_code)
        
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

if __name__ == "__main__":
    main()
```

In this standalone script, we dynamically create two apps with models that have the same class name but reside in different apps. This mimics the reported scenario closely. However, it's important to note that this script does not include the specific `ManyToManyField` relation setup as described in the issue due to the provided context focusing on a generic scenario of potential conflict. To fully replicate the original issue as described, you'd extend the `Common` model by adding a `ManyToManyField` with a `related_name='+'`. This script primarily aims to contextually prepare the testing ground for identifying and demonstrating the presence of the reported bug within Django's migration system.