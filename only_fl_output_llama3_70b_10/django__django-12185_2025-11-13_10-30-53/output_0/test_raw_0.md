Here is the `reproducer.py` file to reproduce the issue:
```
import os
from django.db import models
from django.db.models import F, Window, Lag, Case, When, Value, BooleanField

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

class Employee(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    salary = models.IntegerField()

Employee.objects.create(name='John', department='Sales', salary=50000)
Employee.objects.create(name='Jane', department='Sales', salary=60000)
Employee.objects.create(name='Bob', department='Marketing', salary=70000)

try:
    employees = Employee.objects.annotate(
        lag=Window(
            expression=Lag(expression='salary', offset=1),
            partition_by=F('department'),
            order_by=[F('salary').asc(), F('name').asc()],
        ),
        is_changed=Case(
            When(salary=F('lag'), then=Value(False)),
            default=Value(True), output_field=BooleanField()
        ),
    )
    employees.all()  # Trigger the query execution
except Exception as e:
    print_stacktrace(e)
    assert False, "NotSupportedError should not be raised"
else:
    print("Issue is fixed")
```
This script creates a simple Django model `Employee` and inserts some sample data. Then it tries to execute a query that uses a window expression in a conditional statement used only in the SELECT clause. If the issue is present, an `AssertionError` should be raised with a stack trace of the error. If the issue is fixed, the script will print "Issue is fixed" and exit with code 0.