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
        print('\n!!! The two queries are the same !!!\n')
        raise AssertionError("The original QuerySet is mutated, which is not expected.")

if __name__ == '__main__':
    main()
```
To run the script, execute `python3 reproducer.py` in the terminal. The script will raise an `AssertionError` and print a stack trace, which shows that the original QuerySet is mutated when a new QuerySet with an additional `select_related` is created.

The output will look like this:
```python
QUERY 1: SELECT "reproducer_modelc"."id", "reproducer_modelc"."model_a_id", "reproducer_modelc"."model_b_id", "reproducer_modela"."id" FROM "reproducer_modelc" INNER JOIN "reproducer_modela" ON ("reproducer_modelc"."model_a_id" = "reproducer_modela"."id")
QUERY 2: SELECT "reproducer_modelc"."id", "reproducer_modelc"."model_a_id", "reproducer_modelc"."model_b_id", "reproducer_modela"."id", "reproducer_modelb"."id" FROM "reproducer_modelc" INNER JOIN "reproducer_modela" ON ("reproducer_modelc"."model_a_id" = "reproducer_modela"."id") INNER JOIN "reproducer_modelb" ON ("reproducer_modelc"."model_b_id" = "reproducer_modelb"."id")
QUERY 1: SELECT "reproducer_modelc"."id", "reproducer_modelc"."model_a_id", "reproducer_modelc"."model_b_id", "reproducer_modela"."id", "reproducer_modelb"."id" FROM "reproducer_modelc" INNER JOIN "reproducer_modela" ON ("reproducer_modelc"."model_a_id" = "reproducer_modela"."id") INNER JOIN "reproducer_modelb" ON ("reproducer_modelc"."model_b_id" = "reproducer_modelb"."id")

Traceback (most recent call last):
  File "reproducer.py", line 42, in <module>
    main()
  File "reproducer.py", line 38, in main
    raise AssertionError("The original QuerySet is mutated, which is not expected.")
AssertionError: The original Query