 I was able to reproduce the issue using the following `reproducer.py` file:

```python
import django
import sys
from django.db import migrations, models

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

def run_migration():
    # Set up an in-memory database for the migration
    django.setup()
    migrations.migration_modules = {
        'posts': migrations.__module__,
    }
    migrations.load_migrations()

    # Run the migration
    applied_migrations = []
    migration = migrations.Migration('posts', '0001_initial.py')
    with migration. Lock():
        applied_migrations.append(migration.name)
        migration.apply(migrations.RunSQL.noop, migrations.RunSQL.noop)

        migration = migrations.Migration('posts', '0002_auto_20230314_1429.py')
        with migration. Lock():
            applied_migrations.append(migration.name)
            migration.apply(
                (lambda,: None),
                (lambda,: None),
                (lambda connection, schema_editor:
                    schema_editor.create_model(
                        name='LookImage',
                        fields=[
                            ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                            ('look', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='posts.Look', verbose_name='LOOK')),
                            ('image_url', models.URLField(blank=True, max_length=10000, null=True)),
                            ('image', models.ImageField(max_length=2000, upload_to='')),
                            ('deleted', models.DateTimeField(editable=False, null=True)),
                            ('created_at', models.DateTimeField(auto_now_add=True)),
                            ('updated_at', models.DateTimeField(auto_now=True)),
                        ],
                        options={
                            'db_table': 'look_image',
                            'order_with_respect_to': 'look',
                            'indexes': [
                                models.Index(fields=['look', '_order']),
                                models.Index(fields=['created_at']),
                                models.Index(fields=['updated_at']),
                            ],
                        },
                    )
                ),
                (lambda connection, schema_editor:
                    schema_editor.add_index(
                        model_name='lookimage',
                        index=models.Index(fields=['look', '_order'], name='look_image_look_id_eaff30_idx'),
                    )
                ),
                (lambda connection, schema_editor:
                    schema_editor.add_index(
                        model_name='lookimage',
                        index=models.Index(fields=['created_at'], name='look_image_created_f746cf_idx'),
                    )
                ),
                (lambda connection, schema_editor:
                    schema_editor.add_index(
                        model_name='lookimage',
                        index=models.Index(fields=['updated_at'], name='look_image_updated_aceaf9_idx'),
                    )
                ),
                (lambda connection, schema_editor:
                    schema_editor.alter_order_with_respect_to(
                        name='lookimage',
                        order_with_respect