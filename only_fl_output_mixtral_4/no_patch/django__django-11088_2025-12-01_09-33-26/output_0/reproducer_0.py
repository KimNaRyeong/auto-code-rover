import sys
import traceback
from django.db import migrations
from django.db import models

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run():
    # Arrange
    INITIAL_MIGRATION = """
    from django.db import migrations

    class Migration(migrations.Migration):

        dependencies = [
        ]

        operations = [
            migrations.CreateModel(
                name='TableOne',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('field1', models.BinaryField(default='')),
                ],
            ),
        ]
    """

    REVERSAL_MIGRATION = """
    from django.db import migrations

    class Migration(migrations.Migration):

        dependencies = [
            ('firstapp', '0001_initial'),
        ]

        operations = [
            migrations.AlterField(
                model_name='tableone',
                name='field1',
                field=models.BinaryField(default=b''),
            ),
        ]
    """

    INITIAL_MIGRATION_MODULE = "firstapp.migrations.0001_initial"
    REVERSAL_MIGRATION_MODULE = "firstapp.migrations.0002_reversal"

    # Act
    try:
        migrations.load_migrations(sys.modules[__name__])
        migrations.migrate(INITIAL_MIGRATION_MODULE)
        migrations.migrate(REVERSAL_MIGRATION_MODULE)
        migrations.migrate(INITIAL_MIGRATION_MODULE)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    run()
