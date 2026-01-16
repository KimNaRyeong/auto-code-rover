# reproducer.py

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

def main():
    from django.core.management import execute_from_command_line
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    try:
        # Dynamically create a Django project
        from django.conf import settings
        settings.configure(
            INSTALLED_APPS=[
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'myapp',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'mydatabase',
                }
            },
            ALLOWED_HOSTS=[],
            SECRET_KEY='reproducer-secret-key',
        )

        django.setup()

        # Define the models and migrations inline
        from django.db import migrations, models
        from django.apps import apps
        from django.db.migrations.executor import MigrationExecutor
        from django.db.backends.base.schema import BaseDatabaseSchemaEditor

        class Tag(models.Model):
            name = models.SlugField(help_text="The tag key.")
            value = models.CharField(max_length=150, help_text="The tag value.")

            class Meta:
                app_label = 'myapp'
                ordering = ["name", "value"]
                constraints = [
                    models.UniqueConstraint(
                        fields=['name', 'value'],
                        name="unique_name_value",
                    )
                ]

        class InitialMigration(migrations.Migration):
            initial = True
            
            dependencies = []

            operations = [
                migrations.CreateModel(
                    name='Tag',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.SlugField(help_text='The tag key.')),
                        ('value', models.CharField(help_text='The tag value.', max_length=200)),
                    ],
                    options={
                        'ordering': ['name', 'value'],
                    },
                ),
                migrations.AddConstraint(
                    model_name='tag',
                    constraint=models.UniqueConstraint(
                        fields=['name', 'value'],
                        name='unique_name_value'
                    ),
                ),
            ]

        # Dynamically create the app and register the model
        myapp_config = apps.get_app_config('myapp')
        myapp_config.models_module = sys.modules[__name__]
        apps.all_models['myapp']['tag'] = Tag
        apps.clear_cache()
        
        # Mock migration to alter the field which causes the issue
        class AlterMigration(migrations.Migration):
            dependencies = [
                ('myapp', '0001_initial')
            ]

            operations = [
                migrations.AlterField(
                    model_name='tag',
                    name='value',
                    field=models.CharField(help_text='The tag value.', max_length=150),
                ),
            ]

        # Apply the initial migration
        executor = MigrationExecutor(connections['default'])
        with connections['default'].schema_editor() as schema_editor:
            InitialMigration("0001_initial", 'myapp').apply(None, schema_editor)

        # Apply the altering migration to reproduce the issue
        with connections['default'].schema_editor() as schema_editor:
            AlterMigration("0002_alter_tag_value", 'myapp').apply(None, schema_editor)
        
        print("Issue not present or fixed.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert "operator prohibited in index expressions" in str(e), "Unexpected error message."

if __name__ == "__main__":
    from django.db import connections
    main()
