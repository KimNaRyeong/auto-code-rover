import pandas as pd
from io import StringIO
import sys
import traceback

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

def reproduce_issue():
    data = """id,name,age
1,Alice,25
2,Bob,30"""
    df = pd.read_csv(StringIO(data))
    original_df = df.copy(deep=True)
    modified_df = df.copy()
    original_df.attrs['key'] = 'value'
    assert modified_df.attrs == original_df.attrs
    print_stacktrace(AssertionError("Expected .attrs to be deep copied"))

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        sys.exit(0)
