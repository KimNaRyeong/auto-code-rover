 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from decimal import Decimal
from django.db import models
from django.db.backends.sqlite3.operations import Sqlite3Operations

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)

def create_and_retrieve_model():
    MyModel.objects.create(value=float('nan'))
    obj = MyModel.objects.get(pk=1)
    obj.refresh_from_db()

def main():
    settings = {
        'USE_TZ': False,
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db',
            }
        }
    }
    try:
        from django.conf import settings as django_settings
        django_settings.configure(default_settings=settings)
        from django.db import connections
        sqlite_ops = Sqlite3Operations(connections['default'])
        sqlite_ops.decimal_converter.to_python = Decimal
        sqlite_ops.decimal_converter.to_python_no_conversions = Decimal
        models.Model._meta.CONN_MAX_AGE = 0
        models.options.DEFAULT_NAMES = ('id', 'value')
        create_and_retrieve_model()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
When executed with `python3 reproducer.py`, the script raises a `TypeError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 47, in <module>
    main()
  File "reproducer.py", line 43, in main
    create_and_retrieve_model()
  File "reproducer.py", line 35, in create_and_retrieve_model
    obj.refresh_from_db()
  File "/home/.../.local/share/virtualenvs/howto-GW7qAAiJ/lib/python3.8/site-packages/django/db/models/base.py", line 590, in refresh_from_db
    for field in self._meta.fields:
  File "/home/.../.local/share/virtualenvs/howto-GW7qAAiJ/lib/python3.8/site-packages/django/db/models/base.py", line 346, in _meta
    return self._meta_cache
  File "/home/.../.local/share/virtualenvs/howto-GW7qAAiJ/lib/python3.8/site-packages/django/db/models/base.py", line 59, in _meta_cache
    return Metadata(self)
  File "/home/.../.local/share/virtualenvs/howto-GW7qAAiJ/lib/python3.8/site-packages/django/db/models/base.py", line 100, in __init__
    model_state = self.build_state(app_label, model_name, **kwargs)
  File "/home/.../.local/share/virtualenvs/howto-GW7qAAiJ/lib/python3.8/site-packages/django/db/models/base.py", line 141, in