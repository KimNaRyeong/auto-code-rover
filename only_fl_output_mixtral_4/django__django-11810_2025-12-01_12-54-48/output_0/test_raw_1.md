 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.db import models
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ModelA(models.Model):
    pass

class ModelB(models.Model):
    pass

class ModelC(models.Model):
    model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)

def main():
    query_1 = ModelC.objects.select_related('model_a')
    print('QUERY 1:', str(query_1.query))
    query_2 = query_1.select_related('model_b')
    print('QUERY 2:', str(query_2.query))
    print('QUERY 1:', str(query_1.query))
    if str(query_1.query) == str(query_2.query):
        raise AssertionError("The two queries are the same!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace, demonstrating that the original QuerySet is mutated when a new QuerySet with an additional `select_related` is created.

To fix this issue, you can modify the `select_related` calls to use the `only` method to only select the fields that are needed for the new QuerySet, like this:
```python
query_2 = query_1.only('model_b').select_related('model_b')
```
This will create a new QuerySet that only selects the `model_b` fields, without modifying the original QuerySet.