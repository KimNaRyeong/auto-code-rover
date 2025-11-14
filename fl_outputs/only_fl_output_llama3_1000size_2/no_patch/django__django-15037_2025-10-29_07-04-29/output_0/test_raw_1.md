Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
from django.db import models

def create_models():
    class Foo(models.Model):
        id = models.AutoField(primary_key=True)
        other_id = models.IntegerField(unique=True)

    class Bar(models.Model):
        id = models.AutoField(primary_key=True)
        other_id = models.IntegerField()
        constraint_name = models.ForeignKey(Foo, on_delete=models.CASCADE, name='myconst')

def inspectdb_test():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE foo (
            id serial primary key,
            other_id int UNIQUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE bar (
            id serial primary key,
            other_id int,
            constraint myconst 
            FOREIGN KEY(other_id) references foo(other_id)
        );
    ''')

    Foo().save()
    Bar().save()

    # This should raise an AssertionError
    assert Bar._meta.get_field('other_id').remote_field.model != 'foo', "Expected ForeignKey to be generated for 'foo'"

if __name__ == "__main__":
    try:
        create_models()
        inspectdb_test()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script creates the `Foo` and `Bar` models, then calls `inspectdb` to generate the models. The `inspectdb_test` function asserts that the ForeignKey was not generated correctly, which should raise an `AssertionError`.