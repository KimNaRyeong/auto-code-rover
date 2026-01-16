import os
import sys
import subprocess

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        raise Exception(result.stderr.decode())

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

def check_migration_detection():
    try:
        project_name = "testproject"
        app_name = "myapp"
        os.makedirs(f"{project_name}/{app_name}/migrations", exist_ok=True)
        open(f"{project_name}/{app_name}/__init__.py", 'a').close()
        open(f"{project_name}/{app_name}/migrations/__init__.py", 'a').close()

        # Create minimal settings.py file
        with open(f"{project_name}/settings.py", 'w') as f:
            f.write("SECRET_KEY = 'fake-key-for-testing'\n")
            f.write("INSTALLED_APPS = ['myapp']\n")
            f.write("DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}\n")

        # Create minimal models.py file with the specified CheckConstraint
        with open(f"{project_name}/{app_name}/models.py", 'w') as f:
            f.write("""
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=1), name="age.should.not.be.less.than.one.")
        ]
""")

        # Initialize Django environment
        sys.path.append(os.path.abspath(project_name))
        os.environ['DJANGO_SETTINGS_MODULE'] = f'{project_name}.settings'
        import django
        django.setup()

        from django.core.management import call_command
        
        # Generate migrations
        call_command('makemigrations', app_name)

        # Check if the migration file was properly detected
        migration_files = os.listdir(f"{project_name}/{app_name}/migrations")
        migration_file = next((f for f in migration_files if f.startswith("0001") and f.endswith(".py")), None)
        if not migration_file:
            raise AssertionError("Migration file not found.")
        
        if "should.not.be.less.than.one" not in migration_file:
            raise AssertionError("The expected migration file with dots in its name was not generated correctly.")
        
        print("Migration file detected successfully. Issue not present or has been resolved.")
        
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    check_migration_detection()
