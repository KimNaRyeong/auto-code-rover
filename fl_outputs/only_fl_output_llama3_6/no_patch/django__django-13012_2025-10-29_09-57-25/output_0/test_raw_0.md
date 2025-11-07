Here is the reproducer script:

```python
import django
from django.db.models import Value, Sum, IntegerField
from django.db.models.functions import ExpressionWrapper

django.setup()

def execQuery(expr):
    expr = ExpressionWrapper(expr, output_field=IntegerField())
    return {'expr_res': expr, 'column_a': 'column_a', 'column_b': 1}.annotate(sum=Sum('column_b'))

try:
    result = execQuery(Value(3))
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected ProgrammingError"
else:
    print("Test passed")
    exit(0)

```

This script sets up the Django environment and defines a function `execQuery` that reproduces the issue. It then calls this function with a constant expression (`Value(3)`) and checks if an exception is raised. If an exception is not raised, it prints "Test passed" and exits with code 0.