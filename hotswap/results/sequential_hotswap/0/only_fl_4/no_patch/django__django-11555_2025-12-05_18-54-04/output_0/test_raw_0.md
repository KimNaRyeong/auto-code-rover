 Here is a standalone Python script `reproducer.py` that attempts to reproduce the issue:
```python
from django.db import models
from django.db.models.base import ModelBase

class ParentModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('-name',)

class ChildModel(ParentModel):
    age = models.IntegerField()

    class Meta:
        ordering = (models.Case(models.When(age__gt=18, then=1), default=2, output_field=models.IntegerField()),)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Create a test database and run migrations
    ParentModel.objects.all().delete()
    ChildModel.objects.all().delete()
    ParentModel.objects.db_table = 'parent_model'
    ChildModel.objects.db_table = 'child_model'
    ParentModel._meta.db_table = 'parent_model'
    ChildModel._meta.db_table = 'child_model'
    ParentModel._meta.managed = False
    ChildModel._meta.managed = False
    ParentModel._meta.app_label = 'test_app'
    ChildModel._meta.app_label = 'test_app'
    ParentModel._meta.abstract = False
    ChildModel._meta.abstract = False
    ParentModel._meta.swapped_inheritance_style = False
    ChildModel._meta.swapped_inheritance_style = False
    ParentModel._meta.concrete_model = ParentModel
    ChildModel._meta.concrete_model = ChildModel
    ParentModel._meta.parents = []
    ChildModel._meta.parents = [ParentModel]
    ParentModel._meta.label = 'test_app', 'parent_model'
    ChildModel._meta.label = 'test_app', 'child_model'
    ParentModel._meta.local_concrete_model = ParentModel
    ChildModel._meta.local_concrete_model = ChildModel
    ParentModel._meta.concrete_models = [ParentModel]
    ChildModel._meta.concrete_models = [ChildModel]
    ParentModel._meta.get_field('name').db_tablespace = ''
    ChildModel._meta.get_field('name').db_tablespace = ''
    ParentModel._meta.get_field('name').db_constraint = ''
    ChildModel._meta.get_field('name').db_constraint = ''
    ParentModel._meta.get_field('name').db_index = True
    ChildModel._meta.get_field('name').db_index = True
    ParentModel._meta.get_field('name').rel = None
    ChildModel._meta.get_field('name').rel = None
    ParentModel._meta.get_field('name').contribute_to_class(ParentModel, 'name')
    ChildModel._meta.get_field('name').contribute_to_class(ChildModel, 'name')
    ParentModel._meta.get_field('name').contribute_to_related_class(ParentModel, 'parentmodel')
    ChildModel._meta.get_field('name').contribute_to_related_class(ChildModel, 'childmodel')
    ParentModel._meta.get_field('name').remote_field = None
    ChildModel._meta.get_field('name').remote_field = None
    ParentModel._meta.get_field('name').attname = 'name'
    ChildModel._meta.get_field('name').attname = 'name'
    ParentModel._meta.get_field('name').column = 'name'
    ChildModel._meta.get_field('name').column = '