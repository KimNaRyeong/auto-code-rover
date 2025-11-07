import django
from django.db.models import Value

def main():
    try:
        x = Value('test')
        y = x._resolve_output_field()
        print(y.validators)
        y.clean('1', model_instance=None)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

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

if __name__ == "__main__":
    try:
        django.setup()  # Initialize Django
        main()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

