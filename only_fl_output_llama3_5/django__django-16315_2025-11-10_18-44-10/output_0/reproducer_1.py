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

def setup_django():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbed.settings')
    from django.conf import settings

try:
    setup_django()
    from testbed.models import ActivityBlackListed

    instances = [ActivityBlackListed(blacklistid=1, sectorid=2)]
    qs = ActivityBlackListed.objects
    try:
        qs.bulk_create(instances, update_conflicts=True, update_fields=["sectorid"], unique_fields=["blacklistid"])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected assertion error"
        exit(0)

except Exception as e:
    print_stacktrace(e)
    assert False, "Expected assertion error"
    exit(1)

print("No exception raised. The issue is likely fixed.")
exit(0)
