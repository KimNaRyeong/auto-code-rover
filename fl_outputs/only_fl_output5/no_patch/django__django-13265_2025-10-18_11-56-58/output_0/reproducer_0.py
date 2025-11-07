import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',  # Allows the script to find the models defined below.
    ],
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()


class Look(models.Model):
    name = models.CharField(max_length=100)


class LookImage(models.Model):
    look = models.ForeignKey(Look, on_delete=models.CASCADE, related_name='images', verbose_name='LOOK')
    image_url = models.URLField(blank=True, null=True, max_length=10000)
    image = models.ImageField(max_length=2000, upload_to='')
    deleted = models.DateTimeField(editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'look_image'
        order_with_respect_to = 'look'
        indexes = [
            models.Index(fields=['look', '_order']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]


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


def check_issue():
    try:
        call_command('makemigrations', __name__, interactive=False, verbosity=0)
        call_command('migrate', interactive=False, verbosity=0)
        print("No issue detected.")
        return True
    except Exception as e:
        print_stacktrace(e)
        return False


if __name__ == '__main__':
    assert not check_issue(), "Issue is present."
    sys.exit(0)
