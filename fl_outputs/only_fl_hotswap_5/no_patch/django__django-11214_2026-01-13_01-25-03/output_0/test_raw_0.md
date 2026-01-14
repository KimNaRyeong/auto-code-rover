 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import django
import sys
from django.db import migrations, models

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def test_issue():
    django.setup()

    # Apply initial migration
    initial_migration = "budgetapp/migrations/0001_initial.py"
    with open(initial_migration) as f:
        exec(compile(f.read(), initial_migration, 'exec'))

    # Perform makemigrations
    with open("manage.py") as f:
        manage_py = f.read()
    manage_py = manage_py.replace("makemigrations", "makemigrations --dry-run")
    with open("manage.py", "w") as f:
        f.write(manage_py)
    with open("budgetapp/models.py") as f:
        exec(compile(f.read(), "budgetapp/models.py", 'exec'))
    with open("manage.py") as f:
        exec(compile(manage_py, "manage.py", 'exec'))

    # Check generated migration
    generated_migration = "budgetapp/migrations/0002_auto_20230329_1501.py"
    with open(generated_migration) as f:
        migration = compile(f.read(), generated_migration, 'exec')
    migration_operations = []
    try:
        exec(migration, {"operations": migration_operations})
    except Exception as e:
        assert False, f"Failed to parse generated migration: {e}"

    expected_operations = [
        migrations.RemoveConstraint(
            model_name='monthlybudget',
            name='check_valid_month',
        ),
        migrations.AddConstraint(
            model_name='monthlybudget',
            constraint=models.CheckConstraint(check=models.Q(month__in=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)), name='check_valid_month'),
        ),
    ]

    assert migration_operations == expected_operations, "Generated migration does not match the expected one"


if __name__ == "__main__":
    try:
        test_issue()
        print("Issue reproduced")
        sys.exit(1)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(0)
```
This script sets up a Django environment, applies the initial migration, performs `makemigrations` with a dry run, and checks the generated migration. If the generated migration matches the expected one, the script raises an `AssertionError`, which is caught and printed with a stack trace. If the script exits with code 0, the issue is fixed.