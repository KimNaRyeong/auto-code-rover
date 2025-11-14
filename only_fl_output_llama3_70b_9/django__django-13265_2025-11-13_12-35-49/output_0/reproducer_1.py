import os
import sys
from django.conf import settings
from django.core.management import call_command
from django.test.utils import get_runner

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

# Set up Django settings
settings.configure(
    INSTALLED_APPS=['app'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

# Create a new Django app
os.makedirs('app', exist_ok=True)
with open(os.path.join('app', '__init__.py'), 'w') as f:
    pass

with open(os.path.join('app', 'models.py'), 'w') as f:
    f.write("from django.db import models\n"
            "class Look(models.Model):\n"
            "    pass\n"
            "\n"
            "class LookImage(models.Model):\n"
            "    look = models.ForeignKey('Look', on_delete=models.CASCADE)\n"
            "    class Meta:\n"
            "        db_table = 'look_image'\n"
            "        order_with_respect_to = 'look'\n"
            "        indexes = [\n"
            "            models.Index(fields=['look', '_order']),\n"
            "            models.Index(fields=['created_at']),\n"
            "            models.Index(fields=['updated_at']),\n"
            "        ]\n")

try:
    # Create a new migration
    call_command('makemigrations', 'app', verbosity=0)

    # Apply the migration
    call_command('migrate', verbosity=0)
except Exception as e:
    print_stacktrace(e)
    assert False, "Migration failed"

print("Migration successful")
sys.exit(0)
