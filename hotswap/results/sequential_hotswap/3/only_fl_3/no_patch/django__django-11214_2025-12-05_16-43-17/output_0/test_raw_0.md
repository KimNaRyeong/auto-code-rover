 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import django
import sys
from django.db import migrations
from django.db.models import CheckConstraint, Q

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_check_constraint_range():
    django.setup()

    # Apply initial migrations
    from sample_app.models import MonthlyBudget
    migrations.migrate('sample_app', initial=True)

    # Check the number of migrations
    migrations_module = sys.modules['sample_app.migrations']
    migrations_operations = migrations_module.MIGRATIONS_MODULES['sample_app'][0][1].operations
    assert len(migrations_operations) == 1, "There should be only one migration operation"

    # Perform makemigrations
    migrations.makemigrations('sample_app')

    # Check the generated migration
    second_migration = migrations_module.MIGRATIONS_MODULES['sample_app'][1][1]
    assert len(second_migration.operations) == 2, "There should be two migration operations"

    remove_constraint_operation = second_migration.operations[0]
    assert isinstance(remove_constraint_operation, migrations.RemoveConstraint), "The first operation should be RemoveConstraint"

    add_constraint_operation = second_migration.operations[1]
    assert isinstance(add_constraint_operation, migrations.AddConstraint), "The second operation should be AddConstraint"

    check_constraint = add_constraint_operation.constraint
    assert isinstance(check_constraint, CheckConstraint), "The constraint should be a CheckConstraint"
    assert check_constraint.check.children[0].children[1].__class__.__name__ == "Q", "The check constraint should contain a Q object"
    assert check_constraint.check.children[0].children[1].children[0].__class__.__name__ == "Range", "The Q object should contain a Range object"
    assert check_constraint.check.children[0].children[1].children[0].start == 1, "The start of the range should be 1"
    assert check_constraint.check.children[0].children[1].children[0].stop == 13, "The stop of the range should be 13"

    # Perform migrate
    migrations.migrate('sample_app')

    # Check the number of migrations
    migrations_module = sys.modules['sample_app.migrations']
    migrations_operations = migrations_module.MIGRATIONS_MODULES['sample_app'][1][1].operations
    assert len(migrations_operations) == 2, "There should be two migration operations"

    # Perform makemigrations again
    migrations.makemigrations('sample_app')

    # Check the generated migration
    third_migration = migrations_module.MIGRATIONS_MODULES['sample_app'][2][1]
    assert len(third_migration.operations) == 2, "There should be two migration operations"

    remove_constraint_operation = third_migration.operations[0]
    assert isinstance(remove_constraint_operation, migrations.RemoveConstraint), "The first operation should be RemoveConstraint"

    add_constraint_operation = third_migration.operations[1]
    assert isinstance(add_constraint_operation, migrations.AddConstraint), "The second operation should be AddConstraint"

    check_constraint = add_constraint_operation.constraint
    assert isinstance(check_constraint, CheckConstraint), "The constraint should be a CheckConstraint"
    assert check_constraint.check.children[0].children[1].__class__.__name__ == "Q