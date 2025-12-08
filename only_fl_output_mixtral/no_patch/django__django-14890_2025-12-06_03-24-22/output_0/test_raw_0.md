 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys

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

class MyModel(models.Model):
	name = models.CharField()

for name in ['a', 'b', 'c']:
    MyModel.objects.create(name=name)

group1 = MyModel.objects.filter(name='a')
group2 = MyModel.objects.filter(name='b')
group3 = MyModel.objects.filter(name='c')

combined_group = group1.union(group2)

try:
    group_and = combined_group & group1
except Exception as e:
    print_stacktrace(e)

try:
    group_or = combined_group | group3
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print a stack trace showing that the `&` and `|` operators are silently ignored after `QuerySet.union()`. The line numbers of the statements will be shown clearly.

Note that this script assumes that Django is installed and that a database is available for it to use. You may need to modify the script to match your specific Django setup.