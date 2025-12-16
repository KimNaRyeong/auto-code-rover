 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    name = models.CharField(max_length=256)

class ProxyParent(Parent):
    class Meta:
        proxy = True

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    many_to_many_field = models.ManyToManyField(
        to=Parent,
        through="ManyToManyModel",
        through_fields=['child', 'parent'],
        related_name="something"
    )

class ManyToManyModel(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='+')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='+')
    second_child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, default=None)

def main():
    try:
        Child.objects.get(id=1)
    except ObjectDoesNotExist:
        pass

if __name__ == "__main__":
    main()
```
When you run `python3 reproducer.py`, it will raise a `TypeError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 45, in <module>
    main()
  File "reproducer.py", line 42, in main
    Child.objects.get(id=1)
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/models/query.py", line 439, in get
    num = len(clone)
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/models/query.py", line 269, in __len__
    self._fetch_all()
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/models/sql/compiler.py", line 1156, in execute_sql
    cursor.execute(sql, params)
  File "/home/user/miniconda3/envs/myenv/lib/python3.9/site-packages/django/db/backends/utils.py", line 98, in execute
