Here is the reproducer script:

```python
import os
from django.db import migrations, models
from django.db.backends.mysql.client import DatabaseClient
from django.db.utils import OperationalError
from reproducer import print_stacktrace

def reproduce_issue():
    # Create a test database with case-insensitive collation
    db_client = DatabaseClient()
    db_client.create_database('test_db', collation='latin1_general_ci')

    # Create the 'city' table in the test database
    class City(models.Model):
        name = models.CharField(max_length=255)
        countrycode = models.ForeignKey('Country', on_delete=models.CASCADE, db_column='countryCode')

    class Country(models.Model):
        pass

    with open('migrations.py', 'w') as f:
        f.write('from django.db import migrations\n')
        f.write('class Migration(migrations.Migration):\n')
        f.write('    dependencies = [\n')
        f.write('        ("my_app", "0001_initial"),\n')
        f.write('    ]\n')
        f.write('    operations = [\n')
        f.write('        migrations.RunSQL("CREATE TABLE city (name VARCHAR(255), countrycode INT)"),\n')
        f.write('    ]\n')

    # Run the migration
    try:
        os.system('python manage.py migrate --database test_db my_app')
    except OperationalError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

    # Check if the issue is fixed
    try:
        os.system('python manage.py migrate --database test_db my_app --fake-initial')
    except OperationalError:
        print("Issue not fixed")
        exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script creates a test database with case-insensitive collation, creates the 'city' table in it, and then runs the migration. If the issue is present, it prints the stack trace and raises an `AssertionError`.