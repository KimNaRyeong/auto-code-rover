from django.forms.fields import DecimalField
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

def test_decimal_validator():
    try:
        DecimalField(max_digits=8, decimal_places=7).clean('0E+1')
        assert False, "DecimalValidator should have raised a ValidationError"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_decimal_validator()
