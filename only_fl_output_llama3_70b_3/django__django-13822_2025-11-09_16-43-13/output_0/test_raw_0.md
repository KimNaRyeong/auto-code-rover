Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys

from django.conf import settings
from django.apps import apps
from django.db import migrations, models

settings.configure(
    INSTALLED_APPS=['app1', 'app2'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m2m_field', models.ManyToManyField(related_name='+', to='app1.MyModel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

class Migration2(migrations.Migration):
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m2m_field', models.ManyToManyField(related_name='+', to='app2.MyModel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

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

try:
    apps.get_app_config('app1').models_module = type('models', (object,), {'MyModel': type('MyModel', (models.Model,), {})})
    apps.get_app_config('app2').models_module = type('models', (object,), {'MyModel': type('MyModel', (models.Model,), {})})

    with open(os.path.join('app1', 'migrations', '0001_initial.py'), 'w') as f:
        f.write('from django.db import migrations, models\n')
        f.write('class Migration(migrations.Migration):\n')
        f.write('    dependencies = []\n')
        f.write('    operations = [\n')
        f.write('        migrations.CreateModel(\n')
        f.write('            name=\'MyModel\',\n')
        f.write('            fields=[\n')
        f.write('                (\'id\', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=\'ID\')),\n')
        f.write('                (\'m2m_field\', models.ManyToManyField(related_name=\'+\', to=\'app1.MyModel\')),\n')
        f.write('            ],\n')
        f.write('            options={\'abstract\': False},\n')
        f.write('        ),\n')
        f.write('    ]\n')

    with open(os.path.join('app2', 'migrations', '0001_initial.py'), 'w') as f:
        f.write('from django.db import migrations, models\n')
        f.write('class Migration(migrations.Migration):\n')
        f.write('    dependencies = []\n')
        f.write('    operations = [\n')
        f.write('        migrations.CreateModel(\n')
        f.write('            name=\'MyModel\',\n')
        f.write('            fields=[\n')
        f.write('                (\'id\', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=\'ID\')),\n')
        f.write('                (\'m2m_field\', models.ManyToManyField(related_name=\'+\', to=\'app2.MyModel\')),\n')
        f.write('            ],\n')
        f.write('            options={\'abstract\': False},\n')
        f.write('        ),\n')
        f.write('    ]\n')

    try:
        migrations.RunPython.noop(apps.get_app_config('app1').label, '0001_initial')
        migrations.RunPython.noop(apps.get_app_config('app2').label, '0001_initial')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error occurred during migration creation")
except Exception as e:
    print_stacktrace(e)
    raise

sys.exit(0)
```
This script creates two Django apps (`app1` and `app2`) with a model named `MyModel` in each app. The model has a ManyToManyField with `related_name='+'`. It then tries to create migrations for these models, which should raise an error due