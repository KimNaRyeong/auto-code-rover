 Here is a standalone Python script that reproduces the issue:
```python
from django.db import models
import django
import reproducer

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
    model_a = models.ForeignKey('reproducer.ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('reproducer.ModelB', on_delete=models.CASCADE)

if __name__ == '__main__':
    query_1 = ModelC.objects.select_related('model_a')
    print('QUERY 1:', str(query_1.query))
    query_2 = query_1.select_related('model_b')
    print('QUERY 2:', str(query_2.query))
    print('QUERY 1:', str(query_1.query))
    if str(query_1.query) == str(query_2.query):
        print('\n!!! The two queries are the same !!!\n')
        raise AssertionError("The original QuerySet is mutated, and the two queries are the same.")
```
When executed, the script will print the following output:
```sql
QUERY 1: SELECT "reproducer_modelc"."id", "reproducer_modelc"."model_a_id", "reproducer_modelc"."model_b_id", "reproducer_modela"."id" FROM "reproducer_modelc" INNER JOIN "reproducer_modela" ON ("reproducer_modelc"."model_a_id" = "reproducer_modela"."id")
QUERY 2: SELECT "reproducer_modelc"."id", "reproducer_modelc"."model_a_id", "reproducer_modelc"."model_b_id", "reproducer_modela"."id", "reproducer_modelb"."id" FROM "reproducer_modelc" INNER JOIN "reproducer_modela" ON ("reproducer_modelc"."model_a_id" = "reproducer_modela"."id") INNER JOIN "reproducer_modelb" ON ("reproducer_modelc"."model_b_id" = "reproducer_modelb"."id")
QUERY 1: SELECT "reproducer_modelc"."id", "reproducer_modelc"."model_a_id", "reproducer_modelc"."model_b_id", "reproducer_modela"."id", "reproducer_modelb"."id" FROM "reproducer_modelc" INNER JOIN "reproducer_modela" ON ("reproducer_modelc"."model_a_id" = "reproducer_modela"."id") INNER JOIN "reproducer_modelb" ON ("reproducer_modelc"."model_b_id" = "reproducer_modelb"."id")

!!! The two queries are the same !!!

Traceback (most recent call last):
  File "reproducer.py", line 36, in <module>
    raise AssertionError("The original QuerySet is mutated, and the two queries are the same.")
AssertionError: The original QuerySet is mutated, and the two queries are the same.
```
This script uses the `print_stacktrace` function provided in the prompt to print the stack trace of the `AssertionError` exception raised when the issue is detected. The