import os
from django.db.models import F, Q
from django.test import TestCase

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

try:
    # This should raise an exception if the issue is present
    MyModel = TestCase.create_test_model('MyModel', 
                                         (('some_field', 'CharField'),), 
                                         module=__name__, 
                                         db_tablespace='')
    obj = MyModel(some_field='ANSsi')
    obj.save()
    MyModel.objects.filter(F('some_field').lower() == 'anssi')
    print("Issue is fixed!")
    exit(0)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is still present")

if __name__ == "__main__":
    try:
        # Run the test
        pass
    except SystemExit as e:
        if e.code != 0:
            raise
