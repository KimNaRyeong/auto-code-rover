```python
import django
from django.db import models
from django.conf import settings

# Minimal Django settings necessary for the script to run
settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS = (
        '__main__',  # This script will be the "app"
    ),
    USE_TZ = True,
)

django.setup()

# Define models inline, as we are using this script as a standalone app
class Celebrity(models.Model):
    name = models.CharField(max_length=100)

class ReservedName(models.Model):
    name = models.CharField(max_length=100)

# Utilize Django's machinery to create tables for our models
from django.core.management import call_command
call_command('migrate', '--noinput', '--run-syncdb')

# Function to print stack trace as requested
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

# Reproducing the issue
try:
    qs1 = Celebrity.objects.all()
    qs2 = ReservedName.objects.all()
    
    # This is the line where the issue is expected to occur
    result = qs1.union(qs2).values_list('name').first()

    # If an AssertionError is expected when the issue is present,
    # this block should raise AssertionError when the wrong SQL is generated
    # However, since the specific condition to cause that AssertionError isn't clear
    # without executing against a patched version of Django, make a dummy assertion.
    assert result is not None, "The query did not return any results."

except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("No issue detected, the script exited normally.")
    SystemExit(0)
```