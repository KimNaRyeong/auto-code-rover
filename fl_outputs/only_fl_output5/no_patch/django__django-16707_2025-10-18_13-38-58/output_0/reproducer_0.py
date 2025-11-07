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

def main():
    from django.forms.fields import DateField

    try:
        input_formats_str = str(DateField().input_formats)
        print(input_formats_str)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to print DateField().input_formats with __str__")
    
    # If the script reaches this point without exceptions, it means the issue is not present
    print("The issue could not be reproduced. `DateField().input_formats` was printed successfully with __str__.")

if __name__ == "__main__":
    main()
