Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import django
from django.db import models
from django.contrib.postgres.indexes import Index

django.setup()

class Author(models.Model):
    name = models.CharField(max_length=100)

index_without_opclasses = Index(fields=['-name'], name='idx')
index_with_opclasses = Index(fields=['name'], name='idx', opclasses=['text_pattern_ops'])

print("Testing index without opclasses...")
create_index_statement = index_without_opclasses.create_sql(Author._meta.db_table, of Author._meta)
assert create_index_statement == 'CREATE INDEX "idx" ON "schema_author" ("name" DESC)', f"Expected CREATE INDEX statement to be 'CREATE INDEX \"idx\" ON \"schema_author\" (\"name\" DESC)', but got {create_index_statement}"
print("Passed.")

print("Testing index with opclasses...")
create_index_statement = index_with_opclasses.create_sql(Author._meta.db_table, of Author._meta)
expected_create_index_statement = 'CREATE INDEX "idx" ON "schema_author" ("name" text_pattern_ops)'
try:
    assert create_index_statement == expected_create_index_statement
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Passed.")
exit(0)
```
This script creates two indexes, one without opclasses and one with opclasses, and checks if the generated CREATE INDEX statements match the expected output. If the issue is present, it will raise an `AssertionError` and print a stack trace of the issue using the provided `print_stacktrace` function.