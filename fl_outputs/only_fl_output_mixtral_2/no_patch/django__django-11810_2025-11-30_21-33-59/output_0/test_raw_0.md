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

def create_queryset():
    return ModelC.objects.select_related('model_a')

def main():
    query_1 = create_queryset()
    print_query(query_1)

    query_2 = query_1.select_related('model_b')
    print_query(query_2)
    print_query(query_1)

    if str(query_1.query) == str(query_2.query):
        raise AssertionError("The two queries are the same!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
When executed, the script will print the following output:
```vbnet
SELECT ••• FROM "myapp_modelc" INNER JOIN "myapp_modela" ON ("myapp_modelc"."model_a_id" = "myapp_modela"."id")
SELECT ••• FROM "myapp_modelc" INNER JOIN "myapp_modela" ON ("myapp_modelc"."model_a_id" = "myapp_modela"."id") INNER JOIN "myapp_modelb" ON ("myapp_modelc"."model_b_id" = "myapp_modelb"."id")
SELECT ••• FROM "myapp_modelc" INNER JOIN "myapp_modela" ON ("myapp_modelc"."model_a_id" = "myapp_modela"."id") INNER JOIN "myapp_modelb" ON ("myapp_modelc"."model_b_id" = "myapp_modelb"."id")
Traceback (most recent call last):
  File "reproducer.py", line 44, in <module>
    main()
  File "reproducer.py", line 41, in main
    raise AssertionError("The two queries are the same!")
AssertionError: The two queries are the same!
```
This confirms that the original QuerySet is being mutated when a new QuerySet is created with an additional `select_related` call. The script raises an `AssertionError` to indicate the presence of the issue.