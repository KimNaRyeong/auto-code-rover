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
    try:
        from django.contrib.auth.models import User
        request = object()
        some_variable = User()
        if hasattr(some_variable, "__getitem__"):
            some_variable["foo"]  # This should raise TypeError
        if hasattr(some_variable, "__iter__"):
            for item in some_variable:  # This should also raise TypeError
                pass
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError"

if __name__ == "__main__":
    main()
