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
        from django.contrib.auth.models import LazyObject
        lazy_object = LazyObject()
        if hasattr(lazy_object, "__getitem__"):
            raise TypeError("LazyObject has __getitem__ attribute")
        if hasattr(lazy_object, "__iter__"):
            raise TypeError("LazyObject is iterable")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected assertion error"

if __name__ == "__main__":
    main()
