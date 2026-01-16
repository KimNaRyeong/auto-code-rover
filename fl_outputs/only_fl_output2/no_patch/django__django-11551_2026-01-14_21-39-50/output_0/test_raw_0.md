```python
# reproducer.py
import sys
from django.core.management import call_command
from django.core import checks
from django.db import models
from django.apps import AppConfig
from django.contrib import admin

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

# Mock PositionField as a normal IntegerField for simplicity
class PositionField(models.IntegerField):
    pass

# Create temporary Django settings
SETTINGS_DICT = {
    'INSTALLED_APPS': ['__main__', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
}

class ReproducerAppConfig(AppConfig):
    name = __name__
    verbose_name = "ReproducerApp"

class Thing(models.Model):
    number = models.IntegerField(default=0)
    order = PositionField()

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ['number', 'order']

def main():
    from django.conf import settings
    settings.configure(**SETTINGS_DICT)
    import django
    django.setup()
    # Inject app config to make the model and admin class recognized by Django
    apps = django.apps.apps
    apps.app_configs[__name__] = ReproducerAppConfig(__name__, apps)
    apps.models_ready = apps.apps_ready = apps.models_ready = apps.ready = False
    apps.clear_cache()
    apps.populate([__name__])
    
    errors = ThingAdmin.check(model=Thing)
    e108_errors = [e for e in errors if e.id == 'admin.E108']
    
    if e108_errors:
        print("The issue is present.")
    else:
        print("The issue is fixed or not present.")
    
    assert not e108_errors, "admin.E108 error raised on fields accessible only via instance."

try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```