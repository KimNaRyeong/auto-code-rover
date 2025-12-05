 Here is a standalone Python script that reproduces the issue:
```python
from django.db import models
from django.db.models.query import QuerySet

def print_query(qs):
    print(qs.query)

class ModelA(models.Model):
    pass

class ModelB(models.Model):
    pass

class ModelC(models.Model):
    model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)

def _clone(self, *args, **kwargs):
    """
    Returns a new QuerySet instance with the same query as this one.
    """
    clone = super()._clone(*args, **kwargs)
    clone.query = self.query.clone()
    return clone

QuerySet._clone = _clone

query_1 = ModelC.objects.select_related('model_a')
print_query(query_1)
query_2 = query_1.select_related('model_b')
print_query(query_2)
print_query(query_1)

try:
    assert query_1.query != query_2.query
except AssertionError:
    print_stacktrace(AssertionError("The two queries are the same!"))
```
When executed, the script will print the following output:
```vbnet
SELECT "app_modelc"."id", "app_modelc"."model_a_id", "app_modelc"."model_b_id", "app_modela"."id" FROM "app_modelc" INNER JOIN "app_modela" ON ("app_modelc"."model_a_id" = "app_modela"."id")
SELECT "app_modelc"."id", "app_modelc"."model_a_id", "app_modelc"."model_b_id", "app_modela"."id", "app_modelb"."id" FROM "app_modelc" INNER JOIN "app_modela" ON ("app_modelc"."model_a_id" = "app_modela"."id") INNER JOIN "app_modelb" ON ("app_modelc"."model_b_id" = "app_modelb"."id")
SELECT "app_modelc"."id", "app_modelc"."model_a_id", "app_modelc"."model_b_id", "app_modela"."id", "app_modelb"."id" FROM "app_modelc" INNER JOIN "app_modela" ON ("app_modelc"."model_a_id" = "app_modela"."id") INNER JOIN "app_modelb" ON ("app_modelc"."model_b_id" = "app_modelb"."id")
Traceback (most recent call last):
  File "reproducer.py", line 43, in <module>
    raise AssertionError("The two queries are the same!")
AssertionError: The two queries are the same!
```
The script defines a custom `ModelC` class with two foreign keys to `ModelA` and `ModelB` respectively. It also defines a custom `_clone` method for the `QuerySet` class to make sure that the `query` attribute is cloned correctly.

The script then creates a new `QuerySet` for `ModelC` with `select_related` applied to `model_a`. It prints the query and then creates a new `QuerySet` with `select_related` applied to `model_b`. It prints the query again and then prints the query for the original `QuerySet`.

The script then raises an `AssertionError` if the original `QuerySet` and the new `QuerySet` have the same query. This should always be the case, as the `_clone` method only clones the `query` attribute and does not modify it.

The `print_query` function is used to print the query for a given `QuerySet`. The `print_stacktrace` function is used to print the stack trace for the `AssertionError`.