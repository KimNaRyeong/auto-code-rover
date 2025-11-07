```python
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Count

def setup_django_environment():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            __name__,  # This will add this file as a Django app.
        ],
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
    )
    django.setup()

    # Creating models dynamically
    class Thing(models.Model):
        class Meta:
            app_label = __name__

    class Related(models.Model):
        thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

        class Meta:
            app_label = __name__

    globals().update(locals())  # Exporting models to the global namespace.

def run_tests():
    try:
        # Setting up the database and creating tables.
        setup_django_environment()
        with django.db.connection.schema_editor() as schema_editor:
            schema_editor.create_model(Thing)
            schema_editor.create_model(Related)

        # Populating the database.
        t = Thing.objects.create()
        Related.objects.bulk_create([Related(thing=t) for _ in range(2)])

        # Running the test queries.
        correct_aggregation = Thing.objects.annotate(rc=Count('related')).order_by('rc').values('id', 'rc')
        assert correct_aggregation[0]['rc'] == 2, "Aggregation with Count and order by 'rc' failed."

        aggregation_with_order_by_related = Thing.objects.annotate(rc=Count('related')).order_by('related').values('id', 'rc')
        assert len(aggregation_with_order_by_related) == 2 and all(x['rc'] == 1 for x in aggregation_with_order_by_related), \
            "Ordering by 'related' broke the aggregation unexpectedly."

        aggregation_with_order_by_random = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')
        assert len(aggregation_with_order_by_random) == 1 and aggregation_with_order_by_random[0]['rc'] == 2, \
            "Ordering by '?' should not break the aggregation."

    except AssertionError as e:
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

if __name__ == '__main__':
    run_tests()
```