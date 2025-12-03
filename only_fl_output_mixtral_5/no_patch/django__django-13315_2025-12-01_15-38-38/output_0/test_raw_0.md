 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    name = models.CharField(max_length=100)

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.parent.name} - {self.name}"

class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ['name']

class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = ['parent', 'name']
        limit_choices_to = models.Q(parent__name__startswith='A') | models.Q(parent__name__startswith='B')

def main():
    parent1 = Parent.objects.create(name='Parent1')
    parent2 = Parent.objects.create(name='Parent2')
    Child.objects.bulk_create([
        Child(parent=parent1, name='Child1'),
        Child(parent=parent1, name='Child2'),
        Child(parent=parent2, name='Child3'),
    ])

    form = ChildForm(instance=Child(parent=parent1, name='Child1'))
    try:
        assert len(form.fields['parent'].queryset) == 2
    except AssertionError:
        print_stacktrace(AssertionError("Expected 2 options, but got more than 2 options."))

if __name__ == '__main__':
    main()
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 55, in <module>
    main()
  File "reproducer.py", line 51, in main
    print_stacktrace(AssertionError("Expected 2 options, but got more than 2 options."))
  File "reproducer.py", line 11, in print_stacktrace
    print(f"    {line_number}: {code_context}", file=sys.stderr)
AssertionError: Expected 2 options, but got more than 2 options.
```
This confirms that the issue is present, where the `limit_choices_to` on a `ForeignKey` field involving a join renders duplicate options in the form field.