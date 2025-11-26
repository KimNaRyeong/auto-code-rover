import django
from django.db.models import Value
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
    assert not hasattr(y, 'validators') or all(validator.limit_value is not None for validator in y.validators), "Issue is present: MaxLengthValidator is granted to CharField with no max_length"
    try:
        y.clean('1', model_instance=None)
    except TypeError as e:
        print_stacktrace(e)
        assert False, "Issue is present: MaxLengthValidator is granted to CharField with no max_length"

if __name__ == "__main__":
    test_resolve_output_field()
