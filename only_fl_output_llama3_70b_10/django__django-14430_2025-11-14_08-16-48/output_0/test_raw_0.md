Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import models
from django.db.models import Sum, Value, Coalesce
from django.test import TestCase

class OrderItem(models.Model):
    quantity = models.IntegerField()

def setup_test_data():
    for i in range(1, 11):
        OrderItem(quantity=i).save()

class ReproducerTestCase(TestCase):
    def test_coalesce_issue(self):
        setup_test_data()
        
        # Test with matched Queryset. Sum will return 50
        result = OrderItem.objects.filter(pk__in=[1]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        self.assertEqual(result['test'], 50)
        
        # Test with unmatched Queryset. Sum will return 0
        result = OrderItem.objects.filter(pk__in=[-1]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        self.assertEqual(result['test'], 0)
        
        # Test with unmatched Queryset (using empty list). EmptyResultSet returned because of empty list. Sum will return NONE
        try:
            result = OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
            self.assertEqual(result['test'], 0)  # This should raise AssertionError if the issue is present
        except AssertionError as e:
            print_stacktrace(e)
            raise SystemExit(1)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'test', '--verbosity=2'])
```
This script sets up a test case with an `OrderItem` model and tests the aggregation with `Coalesce` using different querysets. The last test case uses an empty list in the `__in` lookup, which should return an `EmptyResultSet` and cause the `Coalesce` to return `None`. If the issue is present, this script will raise an `AssertionError` and print a stack trace of the issue.