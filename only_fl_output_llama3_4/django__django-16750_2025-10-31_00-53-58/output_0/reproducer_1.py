import django
from django.db import models

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
        from django.db import models
        class Author(models.Model):
            pass
        
        Author.objects.annotate(first_letter=models.Value('M').expression(models.Func(models.Value(77), 'chr')))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected ValueError")

if __name__ == "__main__":
    main()
