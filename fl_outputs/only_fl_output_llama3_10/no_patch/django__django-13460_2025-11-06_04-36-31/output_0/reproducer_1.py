import gettext
from django.utils.translation import gettext as _

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
    person = {'distance_in_miles': 3.14}
    counter = float(person['distance_in_miles'])
    
    try:
        _("%(counter)s mile away" % {"counter": counter})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected no exception, but got one")

if __name__ == "__main__":
    main()
