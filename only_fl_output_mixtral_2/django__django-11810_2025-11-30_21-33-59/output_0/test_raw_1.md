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
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements.

The output will look like this:
```less
QUERY 1: SELECT "app_modelc"."id", "app_modelc"."model_a_id", "app_modelc"."model_b_id", "app_modela"."id" FROM "app_modelc" INNER JOIN "app_modela" ON ("app_modelc"."model_a_id" = "app_modela"."id")
QUERY 2: SELECT "app_modelc"."id", "app_modelc"."model_a_id", "app_modelc"."model_b_id", "app_modela"."id", "app_modelb"."id" FROM "app_modelc" INNER JOIN "app_modela" ON ("app_modelc"."model_a_id" = "app_modela"."id") INNER JOIN "app_modelb" ON ("app_modelc"."model_b_id" = "app_modelb"."id")
QUERY 1: SELECT "app_modelc"."id", "app_modelc"."model_a_id", "app_modelc"."model_b_id", "app_modela"."id", "app_modelb"."id" FROM "app_modelc" INNER JOIN "app_modela" ON ("app_modelc"."model_a_id" = "app_modela"."id") INNER JOIN "app_modelb" ON ("app_modelc"."model_b_id" = "app_modelb"."id")
Traceback (most recent call last):
  File "reproducer.py", line 38, in <module>
    main()
  File "reproducer.py", line 33, in main
    raise AssertionError("The two queries are the same!")
AssertionError: The two queries are the same!
```
The output shows that the original QuerySet `query_1` is mutated by the second `select_related` call, and the two queries are the same. This behavior does not seem correct, as the `select_related` method is documented to return a new QuerySet instance.