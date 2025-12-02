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
        app_label = "testapp"

def main():
    query_string = "?name__in=johnny,viola,gordon,"
    lookup_key, lookup_value = prepare_lookup_value(query_string[1:])
    assert lookup_value == ("johnny", "viola", "gordon",), "The lookup value should not split the last comma"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
To execute the script, run `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.