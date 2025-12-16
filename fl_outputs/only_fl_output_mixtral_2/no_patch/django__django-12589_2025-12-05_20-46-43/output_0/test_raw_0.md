 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sqlite3
from django.db import models
from django.db.models import Count, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce

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

def main():
    # Connect to a SQLite database for testing
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create the tables
    cursor.executescript("""
        CREATE TABLE "a" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "bs_a_id" integer,
            "bs_b_id" integer,
            "bs_status" integer,
            "c_a_id" integer,
            "c_status" integer,
            FOREIGN KEY("bs_a_id","bs_b_id") REFERENCES "ab"("a_id","b_id"),
            FOREIGN KEY("c_a_id") REFERENCES "c"("a_id")
        );
        CREATE TABLE "ab" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "a_id" integer NOT NULL,
            "b_id" integer NOT NULL,
            "status" integer NOT NULL,
            FOREIGN KEY("a_id") REFERENCES "a"("id"),
            FOREIGN KEY("b_id") REFERENCES "b"("id")
        );
        CREATE TABLE "b" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT
        );
        CREATE TABLE "c" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "a_id" integer,
            "status" integer NOT NULL
        );
    """)

    # Insert some test data
    cursor.executemany("""
        INSERT INTO "a" ("bs_a_id", "bs_b_id", "bs_status", "c_a_id", "c_status")
        VALUES (?, ?, ?, ?, ?);
    """, [
        (1, 1, 1, 1, 1),
        (1, 1, 1, 1, 2),
        (1, 1, 1, 2, 1),
        (1, 1, 1, 2, 2),
        (1, 2, 2, 3, 1),
        (1, 2, 2, 3, 2),
        (2, 1, 1, 4, 1),
       