import django
from django.db import models, connections
from django.core.exceptions import AssertionError

def main():
    try:
        # Define the models
        class M1(models.Model):
            id = models.AutoField(primary_key=True, blank=True, null=True)
            f1 = models.TextField(blank=True, null=True)

            class Meta:
                managed = False
                db_table = 'm1'

        class M2(models.Model):
            id = models.AutoField(primary_key=True, blank=True, null=True)
            f2 = models.TextField(blank=True, null=True)

            class Meta:
                managed = False
                db_table = 'm2'

        class M3(models.Model):
            id = models.AutoField(primary_key=True, blank=True, null=True)
            f3 = models.TextField(blank=True, null=True)

            class Meta:
                managed = False
                db_table = 'm3'

        # Create test database connection
        connections.create_test_db(autoclose=False)

        o1 = M2.objects.using('default')
        o2 = M1.objects.using('default')
        u1 = o1.union(o2)
        q = u1.order_by('-f2')
        o3 = M3.objects.using('default')
        res = q.union(o3)

        # Try to count the results
        print(res.count())
    except Exception as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
