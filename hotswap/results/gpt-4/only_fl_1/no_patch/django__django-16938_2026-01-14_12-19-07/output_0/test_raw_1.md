```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core.exceptions import FieldError
from django.db import models, migrations, connection
from django.core.management.color import no_style

# Minimal settings required for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}},
    INSTALLED_APPS=["__main__"],  # This script is the app
    SECRET_KEY='foo',  # Required in Django 1.8+
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Model definitions
class TestTagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("master")

class TestTagMaster(models.Model):
    name = models.CharField(max_length=120)

class TestTag(models.Model):
    objects = TestTagManager()
    name = models.CharField(max_length=120)
    master = models.ForeignKey(TestTagMaster, on_delete=models.SET_NULL, null=True)

class Test(models.Model):
    name = models.CharField(max_length=120)
    tags = models.ManyToManyField(TestTag, blank=True)

# Function to dynamically create and apply the migrations needed for our test models
def create_and_apply_migrations():
    migration_classes = []

    # Generate migration operations for each test model
    for model in [TestTagMaster, TestTag, Test]:
        operations = [migrations.CreateModel(name=model.__name__, fields=[(f.name, f) for f in model._meta.fields])]
        migration = type(f"Migration_{model.__name__}", (migrations.Migration,), {"dependencies": [], "operations": operations})
        migration_classes.append(migration)

    # Apply each migration
    for migration_class in migration_classes:
        migration = migration_class("0001_initial", "__main__")
        executor = migrations.MigrationExecutor(connection)
        executor.loader.build_graph()  # Reload the migration graph
        with connection.schema_editor() as schema_editor:
            state = migrations.state.ProjectState.from_apps(django.apps.apps)
            migration.apply(state, schema_editor)
            sequence_sql = connection.ops.sequence_reset_sql(no_style(), [model for model in [TestTagMaster, TestTag, Test]])
            for sql in sequence_sql:
                schema_editor.execute(sql)

# Function to print stack trace, as provided
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

# Function to reproduce the issue
def reproduce_issue():
    from django.core import serializers
    
    # Creating and applying migrations to ensure the database schema is correct
    create_and_apply_migrations()

    # Creating instances for serialization test
    master = TestTagMaster.objects.create(name='Master Tag')
    tag = TestTag.objects.create(name='Sample Tag', master=master)
    test = Test.objects.create(name='Test Object')
    test.tags.add(tag)

    try:
        output = serializers.serialize("json", [test])
    except FieldError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced: Serialization with select_related in custom manager failed.") from e
    else:
        print("No issue found: Serialization succeeded.", output)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as error:
        print(error)
        exit(1)  # Exit with a non-zero code to indicate the issue was reproduced
    exit(0)  # If the script reaches here, exit with code 0 indicating the issue wasn't reproduced or was fixed
```