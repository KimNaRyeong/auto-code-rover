import sys
from django.core.exceptions import AssertionError
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet

class ParentModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('-name',)

    @classmethod
    def get_order_dir(cls, field_name):
        assert isinstance(field_name, str), "field_name must be a string"
        return super().get_order_dir(field_name)

class ChildModel(ParentModel):
    value = models.IntegerField()

    class Meta:
        ordering = (models.Case(models.When(value=0, then=1), default=0, output_field=models.IntegerField()),)

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    ChildModel.objects.all().order_by('-value')

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
