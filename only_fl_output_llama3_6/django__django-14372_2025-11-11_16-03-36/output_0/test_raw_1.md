Here is the reproducer script:

```python
import os
from django.db import models
from django.core.files.base import ContentFile

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

def reproduce_issue():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    from django.core.files.base import ContentFile
    from django.db import models

    class MyModel(models.Model):
        file_field = models.FileField(upload_to='uploads/')

    my_model = MyModel()
    file_path = os.path.join(os.getcwd(), 'test.txt')
    with open(file_path, 'w') as f:
        f.write('Test content')

    try:
        file_content = ContentFile(open(file_path, 'rb').read())
        my_model.file_field.save('test.txt', file_content)
        my_model.save()
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()

```

This script sets the DJANGO_SETTINGS_MODULE environment variable before importing Django models. This should allow the script to run without throwing an ImproperlyConfigured exception.

Please note that you need to create a `reproducer/settings.py` file in the same directory as this script, with at least an empty settings class:

```python
import os

from django.conf.global_settings import LOGGING

class Settings:
    DEBUG = True
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = 'your_secret_key_here'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    LOGGING = LOGGING
```

You can replace `'your_secret_key_here'` with any valid secret key.