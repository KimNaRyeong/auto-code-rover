import os
import sys
from django.core.management import execute_from_command_line

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

# Create a new Django project
if not os.path.exists("testproj"):
    os.makedirs("testproj")
os.chdir("testproj")

# Create an app with two migrations and squash them
if not os.path.exists("testapp"):
    os.makedirs("testapp")
with open("testapp/models.py", "w") as f:
    f.write("from django.db import models\n\nclass Thing(models.Model):\n    pass")
os.system("python manage.py startapp testapp")
os.system("python manage.py makemigrations testapp --empty")
os.system("python manage.py makemigrations testapp --empty")
os.system("python manage.py squashmigrations testapp 0002")

# Try to migrate backward to a replaced migration
try:
    execute_from_command_line(['manage.py', 'migrate', 'testproj', '0001_initial'])
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")

print("Issue is fixed")
sys.exit(0)
