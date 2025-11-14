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
    class LazyObject:
        def __getitem__(self, item):
            pass

        def __iter__(self):
            pass

    lazy = LazyObject()
    try:
        if hasattr(lazy, "__getitem__"):
            lazy["foo"]
        if hasattr(lazy, "__iter__"):
            for _ in lazy:
                pass
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected error"

if __name__ == "__main__":
    main()
