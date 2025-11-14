import os
import sys

from django.db import models
from django.conf import settings
from django.apps.config import AppConfig

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

settings.configure(
    INSTALLED_APPS=['app1', 'app2'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

class App1Config(AppConfig):
    name = 'app1'
    verbose_name = "App 1"

class App2Config(AppConfig):
    name = 'app2'
    verbose_name = "App 2"

sys.modules['app1'] = sys.modules['app2'] = None

os.makedirs('app1', exist_ok=True)
os.makedirs('app2', exist_ok=True)

with open('app1/models.py', 'w') as f:
    f.write("""
from django.db import models

class MyModel(models.Model):
    m2m_field = models.ManyToManyField('app2.MyModel', related_name='+')
""")

with open('app2/models.py', 'w') as f:
    f.write("""
from django.db import models

class MyModel(models.Model):
    m2m_field = models.ManyToManyField('app1.MyModel', related_name='+')
""")

try:
    from django.core.management import call_command
    call_command('makemigrations', 'app1')
    call_command('makemigrations', 'app2')
except Exception as e:
    print_stacktrace(e)
    assert False, "Error occurred while creating migrations"
else:
    sys.exit(0)
