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

def test_format_html():
    from django.utils.html import format_html

    try:
        # This should raise a TypeError when the issue is fixed
        format_html(f"<i>{'test'}</i>")
        assert False, "Expected TypeError for deprecated format_html call"
    except TypeError as e:
        print_stacktrace(e)
        return 0

if __name__ == "__main__":
    test_format_html()
