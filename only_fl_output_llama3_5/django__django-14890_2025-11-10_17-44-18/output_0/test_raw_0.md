Here is the reproducer script:

```python
import django
from django.db.models import Q
from django.db.models.query import QuerySet

def main():
    try:
        class MyModel(django.db.models.Model):
            name = django.db.models.CharField(max_length=255)

        for name in ['a', 'b', 'c']:
            MyModel.objects.create(name=name)

        group1 = MyModel.objects.filter(name='a')
        group2 = MyModel.objects.filter(name='b')
        group3 = MyModel.objects.filter(name='c')

        combined_group = group1.union(group2)
        group_and = combined_group & group1
        group_or = combined_group | group3

        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script should be saved in a file named `reproducer.py` and run with the command `python3 reproducer.py`.