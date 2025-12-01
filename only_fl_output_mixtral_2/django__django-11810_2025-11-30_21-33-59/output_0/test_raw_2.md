 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db import models
import django
from django.core.exceptions import AssertionError

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

django.setup()

class ModelA(models.Model):
    pass

class ModelB(models.Model):
    pass

class ModelC(models.Model):
    model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)

if __name__ == '__main__':
    query_1 = ModelC.objects.select_related('model_a')
    print('QUERY 1:', str(query_1.query))
    query_2 = query_1.select_related('model_b')
    print('QUERY 2:', str(query_2.query))
    print('QUERY 1:', str(query_1.query))
    if str(query_1.query) == str(query_2.query):
        raise AssertionError("The two queries are the same!")
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.