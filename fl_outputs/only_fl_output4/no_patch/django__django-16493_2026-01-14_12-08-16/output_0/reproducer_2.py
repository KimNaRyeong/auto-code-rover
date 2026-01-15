# reproducer.py
import django
from django.db import models
from django.core.files.storage import FileSystemStorage, default_storage
from django.conf import settings
import random
import sys

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # Acting as a standalone app for this test
    ],
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

django.setup()

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

other_storage = FileSystemStorage(location='/tmp/media/other')

def get_storage():
    return random.choice([default_storage, other_storage])

class MyModel(models.Model):
    my_file = models.FileField(storage=get_storage)

try:
    name, path, args, kwargs = MyModel._meta.get_field('my_file').deconstruct()

    # Validate the 'storage' attribute in 'kwargs' to check if it points to 'get_storage'
    # It's expected that 'storage' is present and equals to the get_storage function
    assert 'storage' in kwargs and kwargs['storage'] == get_storage, \
           "The 'storage' argument in deconstructed field does not reference 'get_storage' function."

    print("Issue not present. Field deconstructed as expected.")
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
