import os
import sys

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

def setup_django_environment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    import django
    django.setup()

def create_models_with_m2m():
    from django.db import models
    from django.apps import apps

    class Meta:
        app_label = 'dynamic_app'

    # Define a dynamic model as reference for M2M
    Base = type('Base', (models.Model,), {'__module__': __name__, 'Meta': Meta})

    # Create two models in different apps with the same name and a ManyToManyField to Base
    for app in ['app1', 'app2']:
        class_name = f'MyModelFrom{app.capitalize()}'
        model_dict = {
            '__module__': __name__,
            'bases': models.ManyToManyField(Base, related_name='+'),
            'Meta': type('Meta', (), {'app_label': app})
        }
        model = type(class_name, (models.Model,), model_dict)
        # Django needs to be aware of the new model
        apps.register_model(app, model)

def make_migrations():
    from django.core.management import call_command
    call_command('makemigrations', 'app1', 'app2', interactive=False, dry_run=True, verbosity=3)

def main():
    try:
        setup_django_environment()
        create_models_with_m2m()
        make_migrations()
        print("No issue detected. Exiting with code 0.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, AssertionError), "An unexpected error occurred."
        # If an AssertionError is raised, we assume it's because of the issue being present

if __name__ == "__main__":
    main()
