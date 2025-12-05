 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import os
import sys
import django
import uuid

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Set up the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')
sys.path.append('..')
django.setup()

# Define the models
import django.db as db
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
class App1Manager(BaseUserManager):
    pass
class App1(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False, verbose_name=_('identifier'))
    text = models.CharField(max_length=100, verbose_name=_('text'))
    another_app = models.UUIDField(null=True, blank=True, verbose_name=_('another app'))
class App2(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False, verbose_name=_('identifier'))
    text = models.CharField(max_length=100, verbose_name=_('text'))
# Change the 'another_app' field to a ForeignKey
App1._meta.get_field('another_app')._unique = False
App1._meta.get_field('another_app').contribute_to_class(App1, 'another_app')
App1._meta.get_field('another_app').remote_field = db.ForeignKey(App2, null=True, blank=True, on_delete=db.SET_NULL)
App1._meta.get_field('another_app').many_to_one = True
App1._meta.get_field('another_app').related_model = App2
App1._meta.get_field('another_app').related_name = 'app1_set'
App1._meta.get_field('another_app').swappable = False
App1._meta.get_field('another_app').default = None

# Create the migration
from django.db import migrations, models
def change_another_app_to_fk(apps, schema_editor):
    App1 = apps.get_model('testapp1', 'App1')
    App1._meta.get_field('another_app')._unique = False
    App1._meta.get_field('another_app').contribute_to_class(App1, 'another_app')
    App1._meta.get_field('another_app').remote_field = models.ForeignKey(App2, null=True, blank=True, on_delete=models.SET_NULL)
    App1._meta.get_field('another_app').many_to_one = True
    App1._meta.get_field('another_app').related_model = App2
    App1._meta.get_field('another_app').related_name = 'app1_set'
    App1._meta.get_field('another_app').swappable = False
    App1._meta.get_field('another_app').default = None
class Migration(migrations.Migration):
    dependencies = [
        ('testapp1', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(change_another_app_to_fk),
    ]

# Apply the migration
from django.core.management import migration
migration.migr