import django
from django.db.models import Value, CharField
from django.core.validators import MaxLengthValidator

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

def test_resolve_output_field():
    x = Value('test')
    y = x._resolve_output_field()
    assert len(y.validators) == 1, "Issue is present: MaxLengthValidator is granted to CharField with max_length=None"
    try:
        y.clean('1', model_instance=None)
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present: MaxLengthValidator cannot work with max_length=None")

if __name__ == "__main__":
    test_resolve_output_field()
