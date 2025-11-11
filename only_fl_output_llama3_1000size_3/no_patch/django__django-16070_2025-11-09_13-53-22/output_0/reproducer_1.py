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
        class SomeModel(models.Model):
            some_foreign_key = models.ForeignKey('SomeOtherModel', on_delete=models.CASCADE, related_name='some_foreign_key')

        SomeModel.objects.all().order_by("non_existing_field")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected FieldError")

if __name__ == "__main__":
    main()
