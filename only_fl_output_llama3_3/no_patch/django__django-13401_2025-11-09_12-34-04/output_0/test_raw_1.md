Here is the reproducer script:

```python
def main():
    from django.db import models

    class A(models.Model):
        class Meta:
            abstract = True
        myfield = models.IntegerField()

    class B(A):
        pass

    class C(A):
        pass

    fields = {B._meta.get_field('myfield'), C._meta.get_field('myfield')}
    assert len(fields) == 1, "Expected one field but got multiple"
    print_stacktrace(Exception("Expected one field but got multiple"))

if __name__ == "__main__":
    main()
```

This script should be executed by `python3 reproducer.py`.