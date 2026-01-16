Given your requirements, I'll provide a Django-based script designed to reproduce the specific issue involving `QuerySet.aggregate()` with annotated fields. This script will attempt to trigger the described issue, handling the raised exception, and printing a stack trace for debug purposes.

Before running this script, ensure you have a Django project set up and can connect to a MySQL database, as that's where this issue is applicable. You should have the `mysqlclient` Python package installed to allow Django to interact with MySQL databases. If not already installed, you can do so by running `pip install mysqlclient`.

Create a file named `reproducer.py` in the root directory of your Django project and paste the following Python code:

```python
import django
from django.conf import settings
from django.db import models
from django.db.models import F, Max, Sum
import os
import sys

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

# Settings configuration (minimal)
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'your_database_host',
            'PORT': 'your_database_port',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # Allows the script to discover models
    ],
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define the model
class T(models.Model):
    foo = models.IntegerField()

    class Meta:
        app_label = '__main__'  # Required for models defined in scripts

def reproduce_issue():
    try:
        # Make sure the table exists
        with django.db.connection.schema_editor() as schema_editor:
            schema_editor.create_model(T)

        T.objects.create(foo=1)  # Insert sample data

        # Attempt to reproduce the issue
        result = T.objects.annotate(anon=F('foo')).aggregate(foo=Max('anon'), sum=Sum('foo'))
        print("Query result:", result)

        assert 'foo' in result, "Expected 'foo' in aggregation result."

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error status

    finally:
        # Clean up by deleting the table
        with django.db.connection.schema_editor() as schema_editor:
            schema_editor.delete_model(T)

        sys.exit(0)  # Normal exit

if __name__ == '__main__':
    reproduce_issue()
```

Make sure to replace `your_database_name`, `your_database_user`, `your_database_password`, `your_database_host`, and `your_database_port` with your MySQL database's actual connection details.

This script will raise an `AssertionError` if the problem occurs as described, printing a stack trace for analysis. When the issue doesn't manifest—it either due to the environment or because it's fixed in a Django version—the script attempts a clean exit with a 0 exit code, indicating success.

Remember, the database and its credentials used in this script should not be exposed in version control systems (e.g., git) for security reasons. Consider using environment variables or other secure methods to manage sensitive information in production or shared environments.