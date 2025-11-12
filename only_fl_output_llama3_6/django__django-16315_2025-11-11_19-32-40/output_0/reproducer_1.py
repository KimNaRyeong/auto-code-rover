import django
from django.db import models
from django.db.models.query import QuerySet

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

def main():
    try:
        class ActivityBlackListed(models.Model):
            class Meta:
                db_table = "Activity_BlackListed"
            blacklistid = models.IntegerField(primary_key=True, db_column="BlacklistID")
            sectorid = models.IntegerField(null=True, blank=True, db_column="SectorID")

        instances = [ActivityBlackListed(blacklistid=i) for i in range(5)]
        QuerySet.bulk_create(instances, update_conflicts=True, update_fields=["sectorid"], unique_fields=["blacklistid"])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception")

if __name__ == "__main__":
    main()
