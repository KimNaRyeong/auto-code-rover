Here is the reproducer script:

```python
import django
from django.db import models
from django.test import TestCase

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Reproducer(TestCase):
    def test_chaining_select_related(self):
        django.setup()
        class ModelA(models.Model):
            pass
        class ModelB(models.Model):
            pass
        class ModelC(models.Model):
            model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
            model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)

        query_1 = ModelC.objects.select_related('model_a')
        print('QUERY 1:', str(query_1.query))
        query_2 = query_1.select_related('model_b')
        print('QUERY 2:', str(query_2.query))
        print('QUERY 1:', str(query_1.query))

        if str(query_1.query) == str(query_2.query):
            raise AssertionError("The two queries are the same")

if __name__ == '__main__':
    try:
        Reproducer().test_chaining_select_related()
    except Exception as e:
        print_stacktrace(e)
        exit(0)
```

This script sets up a Django project, defines three models (ModelA, ModelB, and ModelC), and then tests the issue by chaining `select_related` calls. If the two queries are the same, it raises an `AssertionError`.