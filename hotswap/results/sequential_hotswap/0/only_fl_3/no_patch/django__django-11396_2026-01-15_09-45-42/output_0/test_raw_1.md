```python
# reproducer.py
import django
from django.conf import settings
from django.db import models
from django.db.models import Value
from django.core.management import execute_from_command_line

# Define Django settings (minimal for running this script)
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'yourdbname',  # You need to replace 'yourdbname' with your database name
            'USER': 'youruser',  # Replace 'youruser' with your database user
            'PASSWORD': 'yourpassword',  # Replace 'yourpassword' with your database password
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

# Define a simple model for demonstration purposes
class MyModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = '__main__'

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

def main():
    execute_from_command_line(['manage.py', 'migrate'])  # Create necessary database tables
    try:
        # Perform the query that is supposed to cause an error
        query = MyModel.objects.annotate(my_column=Value('asdf')).order_by('my_column').values_list('id')
        list(query)  # Evaluate the queryset to trigger the query execution
        raise AssertionError("The expected issue did not occur.")
    except Exception as e:
        if "ProgrammingError" in str(e.__class__.__name__):
            print("Issue reproduced successfully: non-integer constant in ORDER BY")
        else:
            print("An unexpected error occurred.", file=sys.stderr)
            print_stacktrace(e)
            sys.exit(1)

if __name__ == '__main__':
    main()

```

Note: Before running this script, make sure you have Django and a PostgreSQL database correctly set up and running. You must replace `'yourdbname'`, `'youruser'`, and `'yourpassword'` with your actual PostgreSQL database name, user, and password. This script configures a bare-minimal Django setting in order to perform the database query that reproduces the issue described.

Since we're directly accessing Django's ORM without a full Django project structure, we manually configure the settings and call `django.setup()` to initialize Django's settings and applications. This allows us to define and use models without a traditional Django project's setup.

Be aware of the PostgreSQL connection configurations. Adjust them as per your local or remote setup to ensure the script can connect successfully to your PostgreSQL instance.