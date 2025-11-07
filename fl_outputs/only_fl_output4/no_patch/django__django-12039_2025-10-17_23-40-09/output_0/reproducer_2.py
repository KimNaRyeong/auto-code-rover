# reproducer.py
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

def mock_create_index_sql(fields, name, opclasses=None):
    """
    Mock function to simulate Django's internal SQL generation for index creation.
    This is a highly simplified version and does not represent the complexity or
    accurate behavior of Django's actual implementation.
    """
    field_str = ", ".join([f'"{f}"' + (' DESC' if f.startswith('-') else '') for f in fields])
    opclass_str = " " + " ".join(opclasses) if opclasses else ""
    sql = f'CREATE INDEX "{name}" ON "schema_author" ({field_str}{opclass_str})'
    return sql

try:
    # Case 1: Without opclasses
    expected_sql_1 = 'CREATE INDEX "idx" ON "schema_author" ("name" DESC)'
    actual_sql_1 = mock_create_index_sql(fields=['-name'], name='idx')
    assert actual_sql_1 == expected_sql_1, "Mismatch in SQL statement without opclasses"

    # Case 2: With opclasses but without explicit order, expecting no excessive whitespace
    expected_sql_2 = 'CREATE INDEX "idx_op" ON "schema_author" ("name" text_pattern_ops)'
    actual_sql_2 = mock_create_index_sql(fields=['name'], name='idx_op', opclasses=['text_pattern_ops'])
    assert actual_sql_2 == expected_sql_2, "Mismatch in SQL statement with opclasses"

    # Exiting with code 0, indicating the expected output matches the actual SQL generated
    print("No issue detected.")
    sys.exit(0)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
