 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.db import models
from django.db.models.sql.compiler import SQLCompiler

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class M1(models.Model):
    id = models.AutoField(primary_key=True,blank=True, null=True)
    f1 = models.TextField(blank=True, null=True) 
    class Meta:
        managed = False
        db_table = 'm1'

class M2(models.Model): 
    id = models.AutoField(primary_key=True,blank=True, null=True)
    f2 = models.TextField(blank=True, null=True) 
    class Meta:
