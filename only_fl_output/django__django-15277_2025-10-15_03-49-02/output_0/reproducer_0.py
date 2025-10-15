# reproducer.py
from django.db.models import Value, CharField
from django.core.exceptions import ValidationError
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

def main():
    try:
        # This mimics the issue where Value objects with string values
        # cause a CharField to be used without specifying `max_length`.
        x = Value('test')
        # Attempt to resolve the output field type, triggering the creation of a CharField
        y = x._resolve_output_field()
        # Demonstrating the validators list contains MaxLengthValidator now.
        assert len(y.validators) > 0, "Expected at least one validator"
        # This should raise a TypeError if `max_length` is None
        try:
            y.clean('1', model_instance=None)
        except ValidationError:
            # Expected behavior after fixing the bug, ValidationError for invalid data, not TypeError
            return 0
        except TypeError as e:
            print_stacktrace(e)
            raise AssertionError("The issue has not been fixed") from e
        
    except AssertionError as e:
        print(e)
        print_stacktrace(e)
        # To ensure that the script exits with a non-zero exit code when the test fails.
        sys.exit(1)

if __name__ == "__main__":
    main()
