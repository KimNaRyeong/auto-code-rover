Here is the reproducer script:

```python
import django
from django.db.models import Value, Sum, IntegerField
from django.db.models.functions import ExpressionWrapper

def execQuery(expr):
    expr = ExpressionWrapper(expr, output_field=IntegerField())
    return django.model.Model.objects.annotate(expr_res=expr).values('expr_res', 'column_a').annotate(sum=Sum('column_b'))

try:
    result = execQuery(Value(3))
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected exception"

print("Issue not present")
exit(0)

```

This script attempts to execute the given query with a constant expression. If an assertion error is raised, it prints the stack trace and exits with code 1.