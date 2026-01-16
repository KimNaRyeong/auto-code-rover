```python
# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models

# Setting up Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    },
    INSTALLED_APPS=[
        '__main__',  # This script is the main module, so we trick Django this way
    ],
    USE_TZ=True,
)
django.setup()


# Defining the model
class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]


class Child(Parent):
    pass


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


# Main script logic
def run_test():
    # Ensuring the tables are created
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Parent)
        schema_editor.create_model(Child)
    
    # Inserting records to create a predictable order
    Parent.objects.create()
    Parent.objects.create()

    # Checking the order
    query = str(Child.objects.all().query)
    expected_order = "ORDER BY \"myapp_parent\".\"id\" DESC"
    if expected_order not in query:
        raise AssertionError(f"Query did not order by DESC as expected. Generated query: {query}")


if __name__ == '__main__':
    try:
        run_test()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with error if an exception is caught
    else:
        print("No issue detected.")
        sys.exit(0)
```

To ensure this script works correctly within a Django context, it's engineered to run standalone by configuring Django settings inline. However, keep in mind that for a real Django project, you would have the models defined within an app and your settings would be already configured through your project's `settings.py`.

Please note that due to how models are dynamically added to apps, the direct string reference `"__main__"` may not work properly in all Django versions especially in more complex or different setups. Adjustments might be necessary depending on the actual environment and Django version in use.