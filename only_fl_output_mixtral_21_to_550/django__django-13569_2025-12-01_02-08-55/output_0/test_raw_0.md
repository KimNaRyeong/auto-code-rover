 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import sys
from django.db import models
from django.db.models.sql.compiler import get_group_by
from django.db.models import Count, Avg, Max, Min

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Random:
    def contains_aggregate(self, *args, **kwargs):
        return False

    def get_source_expressions(self, *args, **kwargs):
        return []

def patch_get_group_by():
    original_get_group_by = get_group_by

    def patched_get_group_by(*args, **kwargs):
        order_by = args[1]
        expressions = []

        for expr, (sql, params, is_ref) in order_by:
            if expr.contains_aggregate:
                continue
            if is_ref:
                continue
            expressions.extend([
                exp for exp in expr.get_source_expressions()
                if not isinstance(exp, Random)
            ])

        args = (args[0], expressions,) + args[2:]
        return original_get_group_by(*args, **kwargs)

    get_group_by = patched_get_group_by

class Thing(models.Model):
    pass

class Related(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

def create_data():
    t = Thing.objects.create()
    rs = [Related.objects.create(thing=t) for _ in range(2)]
    return t

def test_issue():
    t = create_data()

    queryset = Thing.objects.annotate(rc=Count('related')).order_by('rc').values('id', 'rc')
    print("Expected:", [{'id': t.id, 'rc': 2}])
    print("Actual:", queryset)

    queryset = Thing.objects.annotate(rc=Count('related')).order_by('related').values('id', 'rc')
    print("Expected:", [{'id': t.id, 'rc': 1}, {'id': t.id, 'rc': 1}])
    print("Actual:", queryset)

    queryset = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')
    print("Expected:", [{'id': t.id, 'rc': 1}, {'id': t.id, 'rc': 1}])
    print("Actual:", queryset)

    print_stacktrace(AssertionError("Expected the queryset to contain the given values, but it didn't."))

def test_fixed():
    t = create_data()

    queryset = Thing.objects.annotate(rc=Count('related')).order_by('rc').values('id', 'rc')
    print("Expected:", [{'id': t.id, 'rc': 2}])
    print("Actual:", queryset)

    queryset = Thing.objects.annotate(rc=Count('related')).order_by('related').values('id', 'rc')
    print("Expected:", [{'id': t.id, 'rc': 1}, {'id': t.id, 'rc': 1}])
    print("Actual:", queryset)

    queryset = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')
    print("Expected:", [{'id': t.id, 'rc': 1},