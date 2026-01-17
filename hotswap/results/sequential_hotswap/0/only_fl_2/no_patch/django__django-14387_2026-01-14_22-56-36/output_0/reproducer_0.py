# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models as db_models


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


# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    TIME_ZONE='UTC',
)

django.setup()


class Buss(db_models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = db_models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = [('jurisdiction', 'name')]
        app_label = '__main__'


def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs


def reproducer():
    # Perform initial setup
    db_models.signals.post_migrate.disconnect(
        dispatch_uid="django.contrib.auth.management.create_permissions"
    )
    db_models.signals.post_migrate.disconnect(
        dispatch_uid="django.contrib.auth.management.create_superuser"
    )
    try:
        db_models.signals.post_migrate.connect(
            lambda *args, **kwargs: Buss.objects.bulk_create([
                Buss(jurisdiction='GB', name=f'GB_{i}'),
                Buss(jurisdiction='Universal', name=f'Universal_{i}'),
                Buss(jurisdiction='Company', name=f'Company_{i}'),
            ] for i in range(10)),
            weak=False
        )
        django.core.management.call_command('migrate', verbosity=0)
        
        expected_gb_count = Buss.objects.filter(jurisdiction='GB').count()
        filtered_count = jurisdiction_qs('GB').filter(jurisdiction='GB').count()
        assert expected_gb_count == filtered_count, f"Expected {expected_gb_count}, got {filtered_count}"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        if os.path.exists(os.path.join(BASE_DIR, 'db.sqlite3')):
            os.remove(os.path.join(BASE_DIR, 'db.sqlite3'))


if __name__ == '__main__':
    reproducer()
