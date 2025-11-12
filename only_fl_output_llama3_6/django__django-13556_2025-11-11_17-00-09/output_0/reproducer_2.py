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
    try:
        def test_func():
            transaction.on_commit(None)  # This should raise an error
            post_save.send(sender='test')  # This will trigger the on_commit function

        test_func()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError: 'NoneType' object is not callable"

if __name__ == "__main__":
    try:
        from django.db import transaction
        from django.db.models.signals import post_save
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        raise

