import sys
from django import setup
from django.conf import settings
from django.forms.fields import DateField

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

settings.configure()
setup()

try:
    df = DateField()
    print(repr(df.input_formats))  # This should work
    str_df_input_formats = str(df.input_formats)  # This should raise a TypeError
    assert isinstance(str_df_input_formats, str), "Issue is present"
except TypeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    sys.exit(0)
