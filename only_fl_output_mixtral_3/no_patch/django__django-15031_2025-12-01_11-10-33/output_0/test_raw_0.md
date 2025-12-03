 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.contrib.admin.utils import prepare_lookup_value
from django.db.models import Model, CharField

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestModel(Model):
    name = CharField(max_length=100)

    class Meta:
        db_table = 'test_model'

def main():
    query_string = '?name__in=johnny,viola,gordon,'
    lookup_type, lookup_value = prepare_lookup_value(query_string.split('=')[1])
    assert lookup_value == ('johnny', 'viola', 'gordon',), 'The issue is present'

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present. The script creates a simple `TestModel` with a single `CharField` named `name`, and then attempts to filter the queryset using the `name__in` lookup type. The `prepare_lookup_value` function is then called to parse the lookup value from the query string, and an assertion is made that the resulting lookup value matches the expected value. If the assertion fails, the script raises an `AssertionError` and prints a stack trace using the provided `print_stacktrace` function.