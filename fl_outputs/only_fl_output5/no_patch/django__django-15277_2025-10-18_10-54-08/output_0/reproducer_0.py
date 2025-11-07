# reproducer.py

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
    from django.db import models
    from django.core.validators import MaxLengthValidator

    # Creating a temporary Django setup
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = '__fake__'

    # Trying to simulate the issue described
    try:
        x = models.Value('test')
        y = x._resolve_output_field()
        assert isinstance(y.validators[0], MaxLengthValidator), "MaxLengthValidator was expected but not found."
        y.full_clean('1', model_instance=None) # This would not raise if the issue is fixed
        assert False, "Issue was not reproduced, AssertionError expected but none occurred."

    except AssertionError as e:
        # If an AssertionError was intentionally raised, the issue was not fixed
        raise e 
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced, unexpected exception occured."

def main():
    try:
        reproduce_issue()
        print("Issue not present, exited with code 0.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
