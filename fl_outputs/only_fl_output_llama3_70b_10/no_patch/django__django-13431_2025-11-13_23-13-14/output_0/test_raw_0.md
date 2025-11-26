Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.db.models import F, Max, Sum

# Create a Django project and app if they don't exist
if not os.path.exists('project'):
    os.makedirs('project')
    with open(os.path.join('project', '__init__.py'), 'w') as f:
        pass
    with open(os.path.join('project', 'settings.py'), 'w') as f:
        f.write("DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'test_db', 'USER': 'root', 'PASSWORD': '', 'HOST': 'localhost'}}\n")
        f.write("INSTALLED_APPS = ['app']\n")

if not os.path.exists('project/app'):
    os.makedirs('project/app')
    with open(os.path.join('project/app', '__init__.py'), 'w') as f:
        pass
    with open(os.path.join('project/app', 'models.py'), 'w') as f:
        f.write("from django.db import models\n")
        f.write("class T(models.Model):\n")
        f.write("    id = models.AutoField(primary_key=True)\n")
        f.write("    foo = models.IntegerField()\n")

# Run the Django migrations to create the database tables
os.system('python3 project/manage.py makemigrations app')
os.system('python3 project/manage.py migrate')

# Define the model and perform the query
from project.app.models import T

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

try:
    result = T.objects.annotate(anon=F('foo')).aggregate(foo=Max(F('anon')), sum=Sum(F('foo')))
    assert 'anon' in [field.name for field in result.query.annotations]
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
    sys.exit(0)
```
This script creates a Django project and app, defines the model `T`, runs the migrations to create the database tables, and then performs the query that reproduces the issue. If the issue is present, it raises an `AssertionError` with a stack trace of the exception. If the issue is fixed, it prints "Issue is fixed" and exits with code 0.