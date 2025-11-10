Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q

def main():
    class Company(models.Model):
        id = models.IntegerField()
        name = models.CharField(max_length=255)
        trade_number = models.CharField(max_length=255)
        country = models.CharField(max_length=255)

    try:
        query1 = Company.objects.only("name").defer("name")
        query2 = Company.objects.only("name").defer("name").defer("country")

        assert len(query1.query.columns) == 1 and query1.query.columns[0].table_name == "company" and query1.query.columns[0].alias == "id"
        assert len(query2.query.columns) == 1 and query2.query.columns[0].table_name == "company" and query2.query.columns[0].alias == "id"

    except AssertionError as e:
        print_stacktrace(e)
        raise

    try:
        query3 = Company.objects.only("name", "country").defer("name")

        assert len(query3.query.columns) == 2 and query3.query.columns[0].table_name == "company" and query3.query.columns[0].alias == "id" and query3.query.columns[1].table_name == "company" and query3.query.columns[1].alias == "country"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a simple Django model, then attempts to create three different queries: one with `only` and `defer`, one with multiple calls to `defer`, and one with `only` and `defer`. It asserts that the generated SQL query is correct for each case. If any of these assertions fail, it prints the stack trace and raises an exception.