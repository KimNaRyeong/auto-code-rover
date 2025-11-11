import decimal
from django.template.defaultfilters import floatformat

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
        floatformat('0.00', 0)
        floatformat(decimal.Decimal('0.00'), 0)
    except ValueError as e:
        print_stacktrace(e)
        assert False, "Issue is present"
    else:
        print("No issue found")

if __name__ == "__main__":
    main()
