# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_test():
    try:
        from django.utils.html import escape as dj_escape
        import html

        test_string = "O'Reilly & <html>"
        expected = html.escape(test_string, quote=True)

        # Checking for backwards incompatible change specifically
        if dj_escape(test_string) == expected:
            print("Django's escape function matches the stdlib's html.escape().")
        else:
            raise AssertionError("Mismatch in Django's escape and stdlib's html.escape() function outputs.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
    sys.exit(0)
