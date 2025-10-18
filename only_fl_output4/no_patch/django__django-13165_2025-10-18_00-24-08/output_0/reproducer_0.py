# reproducer.py
import os
import django
from django.db import models
from django.db.models import F, FloatField, ExpressionWrapper, Sum, Avg
from django.conf import settings

# Minimal Django setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # Magic trick to enable models creation without creating an app
    ),
    USE_TZ=True,
)

django.setup()

# Model definition
class Hindsight(models.Model):
    pass

class Mallets(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=True)
    hindsight = models.ForeignKey(Hindsight, models.DO_NOTHING, blank=True, null=True)
    believer = models.IntegerField(blank=True, null=True)
    damnably = models.IntegerField(blank=True, null=True)
    issue = models.IntegerField(blank=True, null=True)
    glover = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'mallets'

# Trying to reproduce the described issue
try:
    # Ensure the tables exist
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(Hindsight)
        schema_editor.create_model(Mallets)

    sheer = ExpressionWrapper((F('issue') / F('id')), output_field=FloatField())
    lacquer = ExpressionWrapper(Avg(F('sheer'), output_field=FloatField()), output_field=FloatField())
    q = Mallets.objects.using('default')
    ret = q.annotate(sheer=sheer).values('sheer').annotate(lacquer=Sum(F('believer'))).order_by('sheer').first()

    # If no exception is raised, assume the issue is fixed
    print("Issue possibly fixed.")
    exit(0)

except Exception as e:
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
    
    print_stacktrace(e)

    # Clean up
    os.remove(os.path.join(BASE_DIR, 'db.sqlite3'))
    raise AssertionError("The issue is still present.")
