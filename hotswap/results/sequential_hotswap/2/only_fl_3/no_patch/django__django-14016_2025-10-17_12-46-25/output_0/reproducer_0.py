# reproducer.py

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

def test_issue():
    from django.db.models import Q
    try:
        q_combined = Q() | Q(x__in={}.keys())
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present: 'TypeError: cannot pickle' when applying | operator to a Q object.")

if __name__ == "__main__":
    test_issue()
    print("No error encountered, issue appears to be fixed.")
