 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sqlite3
from django.db import models
from django.db.models import Count, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce

class A(models.Model):
    bs = models.ManyToManyField('B',
                                 related_name="a",
                                 through="AB")

class B(models.Model):
    pass

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="ab_a")
    b = models.ForeignKey(B, on_delete=models.CASCADE, related_name="ab_b")
    status = models.IntegerField()

class C(models.Model):
    a = models.ForeignKey(
        A,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="c",
        verbose_name=_("a")
    )
    status = models.IntegerField()

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Connect to a SQLite database
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create the tables
    cursor.executescript("""
        CREATE TABLE "a" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "bs_a_id" integer NOT NULL REFERENCES "b" ("id") DEFERRABLE INITIALLY DEFERRED,
            "bs_b_id" integer NOT NULL REFERENCES "b" ("id") DEFERRABLE INITIALLY DEFERRED,
            "bs_status" integer NOT NULL
        );
        CREATE TABLE "b" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "ab_a_id" integer NOT NULL REFERENCES "a" ("id") DEFERRABLE INITIALLY DEFERRED,
            "ab_b_id" integer NOT NULL REFERENCES "a" ("id") DEFERRABLE INITIALLY DEFERRED,
            "ab_status" integer NOT NULL
        );
        CREATE TABLE "c" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "a_id" integer REFERENCES "a" ("id") DEFERRABLE INITIALLY DEFERRED,
            "c_status" integer NOT NULL
        );
    """)

    # Insert some test data
    cursor.executescript("""
        INSERT INTO "b" ("id", "ab_a_id", "ab_b_id", "ab_status") VALUES (1, 1, 1, 1);
        INSERT INTO "a" ("id", "bs_a_id", "bs_b_id", "bs_status") VALUES (1, 1, 1, 1);
        INSERT INTO "c" ("id", "a_id", "c_status") VALUES (1, 1, 1);
    """)

    # Create the Django models
    models.ModelBase.metadata.clear()
    models.migrations.executor.ExecutorWalWriteAheadLogging.using = "sqlite"
    models.migrations.executor.Executor.loader_module = "django.db.backends.sqlite3"
    models.migrations.executor