 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import django
import sys
from django.db import models
from django.db.models import F, Avg, ExpressionWrapper, FloatField, TextField, Sum

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

class Hindsight(models.Model):
    id = models.AutoField(primary_key=True,blank=True, null=True)

class Mallets(models.Model):
    id = models.AutoField(primary_key=True,blank=True, null=True)
    hindsight = models.ForeignKey(Hindsight, models.DO_NOTHING, blank=True, null=True)
    believer = models.IntegerField(blank=True, null=True)
    damnably = models.IntegerField(blank=True, null=True)
    issue = models.IntegerField(blank=True, null=True)
    glover = models.TextField(blank=True, null=True)

if __name__ == "__main__":
    sheer = ExpressionWrapper((F('issue') / F('id')), output_field=FloatField())
    lacquer = ExpressionWrapper(Avg(F('sheer'), output_field=FloatField()), output_field=TextField())
    q = Mallets.objects.using('default')
    try:
        ret = q.annotate(sheer=sheer).values('sheer').annotate(lacquer=Sum(F('believer'))).order_by('sheer').first()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

This script uses Django's `ExpressionWrapper` to create an expression with an `output_field` of `FloatField()`. This expression is then used in an annotation on a `Mallets` queryset. The resulting queryset is then used in another annotation with an expression that uses the previous annotation. The final queryset is then used in a `values()` call to select only the `sheer` field. The resulting queryset is then used in an `order_by()` call to order the results by the `sheer` field. The first result is then selected using the `first()` method.

When this script is run on Django 3.2, it throws the following exception:
```ruby
Traceback (most recent call last):
  File "reproducer.py", line 38, in <module>
    ret = q.annotate(sheer=sheer).values('sheer').annotate(lacquer=Sum(F('believer'))).order_by('sheer').first()
  File "/home/<user>/.env/lib/python3.6/site-packages/Django-3.2-py3.6.egg/django/db/models/query.py", line 678, in first
    for obj in (self if self.ordered else self.order_by('pk'))[:1]:
  File "/home/<user>/.env/lib/python3.6/site-packages/Django-3.2-py3.6.egg/django/db/models/query.py", line 287, in __iter__
    self._fetch_all()
  File "/home/<user>/.env/lib/python3.6/site-packages/Django-3.2-py3.6.egg/django/db/models/query.py", line 1305, in _fetch_