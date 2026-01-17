Creating a Python script to reproduce the described issue in Django involves generating a simple Django project setup within the script, running migrations, and inspecting the database schema to confirm the type of columns created for a ManyToManyField relation. This script is designed for PostgreSQL as the database backend since the issue pertains to the handling of `PositiveBigIntegerField` ids, which is specific to PostgreSQL's handling of big integers in ManyToMany relations.

Please ensure you have Django and Psycopg2 installed in your Python environment, as this script uses PostgreSQL. You can install them using pip:

```bash
pip install django psycopg2-binary
```

Adjust the `DATABASES` settings in the script to match your PostgreSQL database credentials.

Now, here's the `reproducer.py`:

```python
"""
reproducer.py

Script to reproduce the issue with ManyToManyField not respecting PositiveBigIntegerField
in an intermediate table in Django with PostgreSQL.
"""

import django
from django.conf import settings
from django.db import models, connections

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

# Setup minimal Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',        # Provide your database name
            'USER': 'your_db_user',        # Provide your database user
            'PASSWORD': 'your_db_password',# Provide your database password
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    SECRET_KEY='a_really_secret_key_you_should_change',
)

django.setup()

# Define the models
class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node, through='RelationNode')

class RelationNode(models.Model):
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    class Meta:
        auto_created = True

# Check the database for correct column types
try:
    with connections['default'].schema_editor() as schema_editor:
        # Apply migrations
        schema_editor.create_model(Node)
        schema_editor.create_model(Relation)
        schema_editor.create_model(RelationNode)

        # Inspect the table to see if it respects PositiveBigIntegerField
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'app_relationnode'
            """)
            column_types = dict(cursor.fetchall())

            assert column_types.get('id') == 'bigint', "ID column type is not bigint."
            assert column_types.get('node_id') == 'bigint', "Node ID column type is not bigint."
            assert column_types.get('relation_id') == 'bigint', "Relation ID column type is not bigint."
            print("Success: All column types are correct. The issue is fixed or could not be reproduced.")

except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script checks if the intermediate table (`RelationNode`) created to manage the `ManyToManyField` relationship between `Node` and `Relation` models correctly uses `bigint` for its id, node_id, and relation_id columns, as expected when using `PositiveBigIntegerField` on PostgreSQL.

Remember to replace `'your_db_name'`, `'your_db_user'`, and `'your_db_password'` with your actual PostgreSQL database credentials. The script assumes local PostgreSQL running on the default port (`5432`).

The Django models are configured, applied migrations, and then the script examines the actual database schema to ensure that the id, node_id, and relation_id columns in the intermediate table are created as `bigint`. If any of these checks fail, the script will print a stack trace and exit with code 1. If the checks pass, indicating that the issue could not be reproduced or has been fixed, it will print a success message and exit with code 0.