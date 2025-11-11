import os
from django.db import models, migrations
from django.core.management import execute_from_command_line
from django.conf import settings

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

def main():
    settings.configure()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
    execute_from_command_line(['manage.py', 'migrate'])

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("SQLite3 migrations can fail when used quoted db_table.")
    else:
        exit(0)

class Migration(migrations.Migration):
    dependencies = [
        ('reproducer', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE TABLE \"new__table_with_quoted_name\" ("
            "\"obj_id\" integer NOT NULL PRIMARY KEY, "
            "\"obj_num\" varchar(20) NULL, "
            "\"country_id\" integer NOT NULL REFERENCES \"countries\" (\"country_id\") DEFERRABLE INITIALLY DEFERRED);"
        ),
    ]

