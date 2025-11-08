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
    data = StringIO("""
Name,Age
Alice,25
Bob,30
""")
    df1 = pd.read_csv(data)
    df2 = df1.copy(deep=True)
    
    assert df1.attrs == df2.attrs
    
    raise AssertionError("Expected .attrs to be deep copied")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
