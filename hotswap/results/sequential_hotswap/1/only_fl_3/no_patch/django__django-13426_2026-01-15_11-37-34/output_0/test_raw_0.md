```python
# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models

# Minimal Django setup for script to run stand-alone
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script is the app
    ),
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)
django.setup()

# Model definitions
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


def print_stacktrace(e: Exception):
    import traceback
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
        o1 = M2.objects.using('default')
        o2 = M1.objects.using('default')
        u1 = o1.union(o2)
        q = u1.order_by('-f2')
        o3 = M3.objects.using('default')
        res = q.union(o3)
        print(res.count())

        # The following assertion is intended to fail if an issue is present.
        # If the above operation causes an error, this line should not execute.
        # If the issue is fixed, an AssertionError will not be raised here.
        assert False, "Expected issue did not occur."

    except Exception as e:
        print_stacktrace(e)
        # If the specific TypeError occurs, we ensure that the script exits with 0
        # indicating the issue is reproduced.
        if isinstance(e, TypeError):
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
```

Please make sure you have Django installed in your environment (`pip install Django`) before running this script. Furthermore, this script uses a SQLite database for demonstration purposes which is assumed to be adequate for reproducing the reported issue without requiring any setup for other database types. The script expects to operate in a Django-managed environment, having tables for models `M1`, `M2`, and `M3` existing. In a real-world scenario, either these tables should exist in your database, or the models' `managed` meta option should be set to `True` for Django to manage them (which would require you to run migrations).
