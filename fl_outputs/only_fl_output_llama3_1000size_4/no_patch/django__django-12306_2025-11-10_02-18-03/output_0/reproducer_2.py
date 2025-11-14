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
    class MultiValueFieldModel:
        choices = (
            ('one', ((1, 'One'), (11, 'Eleven'))),
            ('two', ((2, 'Two'), (22, 'Twenty two'))),
        )

    try:
        from django.db import models
        model = type('Model', (), {'choices': MultiValueFieldModel.choices})
        if not isinstance(model.choices, list):
            raise AssertionError("Expected a list")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
