# reproducer.py
import os
import sys

def setup_django_env():
    from django.conf import settings
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=('__main__',),
        SECRET_KEY='fake-key',
        BASE_DIR=os.path.dirname(os.path.abspath(__file__)),
    )

    import django
    django.setup()

# Define custom print stacktrace function as instructed
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

# Callable for FilePathField 'path' argument
def dynamic_path():
    from django.conf import settings
    return os.path.join(settings.BASE_DIR, 'example_dir')

def reproduce_issue():
    # Setup Django environment
    setup_django_env()

    from django.db import models

    # Define a model class dynamically to test FilePathField with callable path
    class TestModel(models.Model):
        name = models.CharField(max_length=255)
        file = models.FilePathField(path=dynamic_path)

        class Meta:
            app_label = '__main__'

    # Attempt to create and apply migrations, should fail if issue is present
    try:
        from django.core.management import call_command
        call_command('makemigrations', '__main__', interactive=False, name='test_migration_callable_path')
        call_command('migrate', '__main__')

        # If no exceptions were raised, assume FilePathField can accept callable without issues
        print("Test passed: `FilePathField` accepts a callable without errors.")
        sys.exit(0)

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed: Django `FilePathField` does not accept callable for dynamic path resolution.") from e

if __name__ == '__main__':
    reproduce_issue()
