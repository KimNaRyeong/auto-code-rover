def simulate_django_debug_view_behaviour():
    try:
        try:
            raise RuntimeError('my error')
        except Exception as exc:
            raise ValueError('my new error') from None
    except ValueError as exc:
        # Returning a tuple indicating whether __cause__ and __context__ are not None
        return (exc.__cause__ is not None, exc.__context__ is not None)

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
        # Simulating Django's debug view exception handling
        cause_present, context_present = simulate_django_debug_view_behaviour()
        # The issue is present if context is not suppressed (__context__ should be None)
        if context_present:
            raise AssertionError("Debug error view doesn't respect exc.__suppress_context__.")
        else:
            print("The issue is fixed: __suppress_context__ is respected.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
