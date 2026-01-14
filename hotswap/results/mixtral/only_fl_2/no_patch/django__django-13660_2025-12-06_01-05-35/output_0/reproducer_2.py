import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def f():
    print(django.__version__)

if __name__ == "__main__":
    try:
        import django
        exec("f()")
    except Exception as e:
        print_stacktrace(e)
        assert False, "An exception should not be raised here."
    else:
        assert False, "django should not be defined here."

    try:
        import django
        exec("f()", {})
    except Exception as e:
        print_stacktrace(e)
        assert True
    else:
        assert False, "django should be undefined here."
