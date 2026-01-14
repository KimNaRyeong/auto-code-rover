import django
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


def run_test():
    # Replace the following settings with your actual settings
    settings = {
        'NAME': ':memory:',
        'INSTALLED_APPS': [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'incidents',
            'vault',
        ],
    }

    try:
        django.setup(**settings)

        from vault.models import Incident as VaultIncident
        from incidents.models import Incident as IncidentsIncident

        # Create models
        VaultIncident.objects.create()
        IncidentsIncident.objects.create()

        # Create M2M relationship
        VaultIncident.objects.first().incidents.add(IncidentsIncident.objects.first())

        # Rename the IncidentsIncident model
        from django.db import migrations

        operations = [
            migrations.RenameModel(
                old_name='Incident',
                new_name='Folder',
            ),
        ]

        m = django.db.migrations.migrations.RunPython(lambda x, y: None, operations)
        m.database_forwards(django.db.migrations.executor.MigrationExecutor(django.db.connections['default']), django.db.migrations.state.RealState())

    except Exception as e:
        print_stacktrace(e)
        assert False, "Test failed"

    assert True, "Test passed"


if __name__ == "__main__":
    run_test()
