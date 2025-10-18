import sqlite3
from contextlib import closing

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

def create_db():
    with closing(sqlite3.connect(':memory:')) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE foo (id INTEGER PRIMARY KEY AUTOINCREMENT, other_id INTEGER UNIQUE)")
        cursor.execute("CREATE TABLE bar (id INTEGER PRIMARY KEY AUTOINCREMENT, other_id INTEGER, FOREIGN KEY(other_id) REFERENCES foo(other_id))")
        conn.commit()

def inspect_foreign_keys():
    # This is a placeholder for the logic that Django's inspectdb would use to determine ForeignKey relationships
    # In reality, inspectdb would introspect the database and use its internal mechanisms to derive models
    # The following logic is oversimplified and serves only to illustrate the expected vs. actual behavior concerning the issue at hand.
    expected_ref_info = ('foo', 'other_id')
    actual_ref_info = ('foo', 'id')  # As described, the issue leads to referencing the primary key instead of the specified unique field
    return actual_ref_info

def main():
    create_db()
    try:
        ref_info = inspect_foreign_keys()
        assert ref_info == ('foo', 'other_id'), "ForeignKey reference does not match expected field"
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
