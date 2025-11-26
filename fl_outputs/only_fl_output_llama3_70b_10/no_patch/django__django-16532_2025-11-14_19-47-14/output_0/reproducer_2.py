import os
import sys

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
    # Create a new Django project and apps
    os.makedirs('incidents', exist_ok=True)
    os.makedirs('vault', exist_ok=True)

    with open('manage.py', 'w') as f:
        f.write("""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
""")

    with open('project/settings.py', 'w') as f:
        f.write("""
INSTALLED_APPS = ['incidents', 'vault']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
""")

    with open('incidents/models.py', 'w') as f:
        f.write("""
from django.db import models

class Incident(models.Model):
    name = models.CharField(max_length=255)
""")

    with open('vault/models.py', 'w') as f:
        f.write("""
from django.db import models
from incidents.models import Incident

class VaultIncident(models.Model):
    incident = models.OneToOneField(Incident, on_delete=models.CASCADE)
""")

    # Run migrations to create the tables
    os.system("python manage.py makemigrations incidents vault")
    os.system("python manage.py migrate")

    # Create a migration that renames the Incident model
    with open('vault/migrations/0001_rename_incident_model.py', 'w') as f:
        f.write("""
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel('Incident', 'OldIncident', table_name='incidents_incident'),
    ]
""")

    # Apply the migration
    os.system("python manage.py migrate vault 0001")

    raise AssertionError("The issue should have been raised by now!")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
