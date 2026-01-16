# reproducer.py

import os
import django
from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.functions import Lag
from django.db.models import Window, FloatField

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

# Define settings for the Django project
settings.configure(
    DEBUG = True,
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS = (
        '__main__',
    ),
    TIME_ZONE = 'UTC',
    USE_TZ = True,
)

django.setup()

# Define the model as per the issue description
class LagTest(models.Model):
    modified = models.DateField()
    data = models.FloatField()
    amount = models.DecimalField(decimal_places=4, max_digits=7)

    class Meta:
        app_label = '__main__'

try:
    # Migrate models
    from django.core.management import call_command
    call_command('migrate')

    # Attempting the problematic query
    w = Window(expression=Lag('amount', 7, output_field=FloatField()), partition_by=[F('modified')], order_by=F('modified').asc())
    q = LagTest.objects.all().annotate(w=w)

    # Trigger query execution to potentially catch the OperationalError
    list(q)  # This forces query evaluation and can raise OperationalError if issue exists
    print("No issue encountered.")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("The issue is present.") from e

