Here is the reproducer script:

```python
import inspectdb
from django.db import models

def create_tables():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE foo (
            id serial primary key, other_id int UNIQUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE bar (
            id serial primary key, other_id int,
            constraint myconst 
            FOREIGN KEY(other_id) references foo(other_id)
        );
    ''')

def inspectdb_test():
    model = inspectdb.inspectdb('bar')
    assert model._meta.get_field('other_id').remote_field.name == 'foo', "Expected foreign key to be 'foo' but got {}".format(model._meta.get_field('other_id').remote_field.name)

if __name__ == "__main__":
    try:
        create_tables()
        inspectdb_test()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script creates the tables, then calls `inspectdb` to generate a model for the 'bar' table. It asserts that the foreign key is correctly set to 'foo'. If the assertion fails (i.e., the issue is present), it prints the stack trace and exits with code 1.