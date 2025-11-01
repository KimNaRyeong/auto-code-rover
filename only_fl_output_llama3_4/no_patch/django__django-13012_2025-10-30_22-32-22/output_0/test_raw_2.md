Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Value, ExpressionWrapper, Sum, IntegerField

def execQuery(expr):
    expr = ExpressionWrapper(expr, output_field=IntegerField())
    return models.Model.objects.annotate(expr_res=expr).values('expr_res', 'column_a').annotate(sum=Sum('column_b'))

try:
    result = execQuery(Value(3))
    query = str(result.query)
    assert "GROUP BY" not in query, f"Expected GROUP BY clause to be omitted, but found it: {query}"
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script sets up the Django environment and defines a function `execQuery` that reproduces the issue. It then attempts to execute this function with a constant expression (`Value(3)`) and checks if the generated query contains the GROUP BY clause. If it does, the test fails by raising an AssertionError.

Please note that you need to have Django installed in your Python environment for this script to work.