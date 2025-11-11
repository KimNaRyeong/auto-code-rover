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

def main():
    x = Value('test')
    y = x._resolve_output_field()
    
    try:
        y.validators = [MaxLengthValidator(None)]
        y.clean('1', model_instance=None)
    except TypeError as e:
        print_stacktrace(e)
        assert False, "Issue is present"
    else:
        print("Issue is fixed")

if __name__ == "__main__":
    main()
