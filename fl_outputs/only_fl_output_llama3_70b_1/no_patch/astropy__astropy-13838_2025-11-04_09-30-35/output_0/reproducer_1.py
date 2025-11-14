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
    from astropy.table import QTable, Column
    table = QTable({'a': [1, 2], 'b': [3, 4]})
    column = Column([5, 6], dtype='int64')
    table.add_column(column)
    assert table['b'].dtype.kind == 'i'  # This should raise an AssertionError if the issue is present
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue is present"
