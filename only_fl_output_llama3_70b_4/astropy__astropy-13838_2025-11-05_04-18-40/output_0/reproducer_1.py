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

try:
    # Add your code here to reproduce the issue
    # For example:
    table = QTable(rows=[{"A": 0, "B": 0}])
    column = Column(name="C", data=[])
    table.add_column(column)
    print(table)  # This should raise an AssertionError if the issue is present
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue is present"
