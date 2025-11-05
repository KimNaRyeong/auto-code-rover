import django
from django.forms import DurationField
from django.utils.dateparse import parse_duration

def main():
    try:
        duration_field = DurationField()
        duration_field.clean('P3(3D')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

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
        from django.conf import settings
        settings.configure()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Django setup failed")
    main()

