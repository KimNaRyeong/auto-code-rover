import sys
import traceback

from django.core.exceptions import AssertionError
from django.db import models
from django.db.models.base import ModelBase

class ParentModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('-name',)

class ChildModel(ParentModel):
    age = models.IntegerField()

    class Meta:
        ordering = (models.Case(models.When(age__gt=18, then=1), default=0, output_field=models.IntegerField()),)

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
    try:
        ChildModel.objects.all().order_by('-age')
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        sys.exit(1)
