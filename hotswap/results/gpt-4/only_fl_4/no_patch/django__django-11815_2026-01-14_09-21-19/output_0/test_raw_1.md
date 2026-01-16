Given the feedback on the initial code and the requirement for a standalone `reproducer.py` file that works correctly within the Django framework, adjustments will be made to properly instantiate Django settings. This is crucial for avoiding errors related to improperly configured Django settings. The updated script will initialize Django settings at the start, allowing `gettext_lazy` to function as expected. Additionally, the script will migrate the database and verify if the default value is using the Enum name rather than its translated value, aiming to reproduce the issue accurately.

```python
# reproducer.py
import os
import sys
from enum import Enum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
import django
from django.conf import settings
from django.db import models
from django.core.management.commands.migrate import Command as MigrateCommand
from django.utils.translation import gettext_lazy as _
from django.apps import apps

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

class Status(Enum):
    GOOD = _('Good')  # 'Good' will be translated
    BAD = _('Bad')  # 'Bad' will be translated

    def __str__(self):
        return self.name

settings.configure(
    INSTALLED_APPS=['__main__'],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_I18N=True,
    LANGUAGE_CODE='en-us',
    MIDDLEWARE=[],
    ROOT_URLCONF=__name__,
)

django.setup()

class Item(models.Model):
    status = models.CharField(default=Status.GOOD.name, max_length=128)

    class Meta:
        app_label = '__main__'

# Manually creating migrations for the Item model
migration = migrations.Migration('initial', 'test_app')
migration.operations = [
    migrations.CreateModel(
        name='Item',
        fields=[
            ('id', models.AutoField(primary_key=True)),
            ('status', models.CharField(default=Status.GOOD.name, max_length=128)),
        ],
    ),
]

# Applying the migrations
executor = MigrateCommand(stdout=sys.stdout, stderr=sys.stderr)
executor.execute_from_command_line(['manage.py', 'migrate'])

try:
    default_status = Item._meta.get_field('status').get_default()
    assert default_status == Status.GOOD.name, "The default value should be the Enum member's name"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("The issue is not present.")
sys.exit(0)
```

This script attempts to create a minimal Django setup programmatically, define a model that uses an enum with translated values for a field's default, and then tests to ensure that the default value logic works correctly. If it encounters an assertion error where the Enum's name is not correctly used as the default, it prints a detailed traceback. This adjusted approach ensures that Django's settings are appropriately configured before they are accessed.